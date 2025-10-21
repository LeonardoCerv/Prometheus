"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import Sidebar from "@/components/sidebar";
import MessageInput from "@/components/MessageInput";
import Dashboard from "@/components/dashboard";
import { db } from "@/lib/firebase";
import { collection, getDocs, addDoc, updateDoc, doc, query, where } from "firebase/firestore";
import { getCurrentUser, isAuthenticated } from "@/lib/auth";

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface Conversation {
  id: string;
  title: string;
  timestamp: Date;
  type: 'job_posting' | 'job_search';
  messages: Message[];
  profiles?: Profile[];
}

interface Profile {
  id: string;
  name: string;
  profilePictureUrl: string;
  briefDescription: string;
  matchScore: number;
  linkedinUrl: string;
  bio: string;
  location?: string;
  currentActivities?: string[];
  projects?: string[];
  achievements?: string[];
  cvUrl?: string;
}

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const chatId = params.id as string;
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState<Profile | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Format message content with proper line breaks and basic markdown
  const formatMessageContent = (content: string) => {
    // Split by double line breaks for paragraphs
    const paragraphs = content.split('\n\n');
    
    return paragraphs.map((paragraph, pIndex) => {
      // Split by single line breaks within paragraphs
      const lines = paragraph.split('\n');
      
      return (
        <div key={pIndex} className={pIndex > 0 ? 'mt-4' : ''}>
          {lines.map((line, lIndex) => {
            // Process bold text (**text**)
            const parts = line.split(/(\*\*.*?\*\*)/g);
            const processedLine = parts.map((part, partIndex) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={partIndex} className="font-bold">{part.slice(2, -2)}</strong>;
              }
              return <span key={partIndex}>{part}</span>;
            });
            
            return (
              <div key={lIndex} className={lIndex > 0 ? 'mt-1' : ''}>
                {processedLine}
              </div>
            );
          })}
        </div>
      );
    });
  };

  const generateAIResponse = async (conv: Conversation, userMessage: Message) => {
    setIsLoading(true);

    try {
      // Call the conversation agent API
      const response = await fetch('/api/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
          conversationId: conv.id,
          resetConversation: false, // Could be enhanced to detect reset commands
        }),
      });

      if (!response.ok) {
        throw new Error(`API responded with status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Conversation API response:', data); // Debug log
      console.log('Response field:', data.response);
      console.log('Profiles field:', data.profiles);
      console.log('Profiles length:', data.profiles ? data.profiles.length : 'undefined');

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: 'ai',
        timestamp: new Date()
      };

      const updatedConversation = {
        ...conv,
        messages: [...conv.messages, aiMessage],
        profiles: data.profiles || []
      };
      setConversation(updatedConversation);
      setProfiles(data.profiles || []);
      console.log('Profiles set:', data.profiles); // Debug log

      // Update Firestore with both messages and profiles
      try {
        await updateDoc(doc(db, "conversations", conv.id), {
          messages: updatedConversation.messages,
          profiles: data.profiles || []
        });
      } catch (error) {
        console.error("Error updating conversation:", error);
      }
    } catch (error) {
      console.error("Error generating AI response:", error);

      // Fallback message
      const fallbackMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm sorry, I'm having trouble connecting to the candidate database right now. Please try again in a moment.",
        sender: 'ai',
        timestamp: new Date()
      };

      const updatedConversation = {
        ...conv,
        messages: [...conv.messages, fallbackMessage],
        profiles: []
      };
      setConversation(updatedConversation);

      // Update Firestore
      try {
        await updateDoc(doc(db, "conversations", conv.id), {
          messages: updatedConversation.messages,
          profiles: []
        });
      } catch (error) {
        console.error("Error updating conversation:", error);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Load conversation from Firestore
  useEffect(() => {
    const loadConversation = async () => {
      try {
        if (!isAuthenticated()) {
          router.push("/");
          return;
        }

        const user = getCurrentUser();
        if (!user) {
          router.push("/");
          return;
        }

        const conversationsRef = collection(db, "conversations");
        const q = query(conversationsRef, where("userId", "==", user.userId));
        const querySnapshot = await getDocs(q);
        const conversations: Conversation[] = [];
        querySnapshot.forEach((doc) => {
          const data = doc.data();
          conversations.push({
            id: doc.id,
            title: data.title,
            timestamp: data.timestamp.toDate(),
            type: data.type,
            messages: data.messages?.map((msg: any) => ({
              ...msg,
              timestamp: msg.timestamp.toDate()
            })) || [],
            profiles: data.profiles || []
          });
        });

        const currentConversation = conversations.find((conv) => conv.id === chatId);
        if (currentConversation) {
          // Check if conversation has messages
          if (currentConversation.messages.length === 0) {
            // Empty conversation, redirect to find
            router.push("/find");
            return;
          }

          setConversation(currentConversation);
          // Load profiles from the conversation
          if (currentConversation.profiles && currentConversation.profiles.length > 0) {
            setProfiles(currentConversation.profiles);
            console.log('Loaded profiles from Firestore:', currentConversation.profiles);
          }

          // Check if we need to generate AI response for the last user message
          const lastMessage = currentConversation.messages[currentConversation.messages.length - 1];
          if (lastMessage && lastMessage.sender === 'user' && !isLoading) {
            // Check if there's no AI response after this user message
            const messages = currentConversation.messages;
            const lastMessageIndex = messages.length - 1;
            const hasAIReply = lastMessageIndex > 0 && messages[lastMessageIndex - 1]?.sender === 'ai';

            if (!hasAIReply) {
              // Generate AI response for the user message
              generateAIResponse(currentConversation, lastMessage);
            }
          }
        } else {
          // Conversation not found, redirect to find
          router.push("/find");
        }
      } catch (error) {
        console.error("Error loading conversations:", error);
        router.push("/find");
      }
    };

    loadConversation();
  }, [chatId, router]);

    // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversation?.messages]);

  const handleProfileClick = (profile: Profile) => {
    setSelectedProfile(profile);
  };

  const sendMessage = async (message: string) => {
    if (!message.trim() || !conversation) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: message.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    // Add user message immediately
    const updatedConversation = {
      ...conversation,
      messages: [...conversation.messages, userMessage]
    };
    setConversation(updatedConversation);

    // Update Firestore (preserve existing profiles)
    try {
      await updateDoc(doc(db, "conversations", conversation.id), {
        messages: updatedConversation.messages,
        profiles: conversation.profiles || []
      });
    } catch (error) {
      console.error("Error updating conversation:", error);
    }

    // Generate AI response
    await generateAIResponse(updatedConversation, userMessage);
  };

  if (!conversation) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted">Loading chat...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Sidebar />
      <main className="flex w-full flex-1 flex-col md:pl-[272px] lg:pr-0">
        <div className="flex flex-col h-screen">
          {/* Chat Header */}
          <div className="border-b border-muted px-8 py-6">
            <h1 className="text-2xl font-semibold text-foreground px-2">{conversation.title}</h1>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
            {conversation.messages.map((msg: Message) => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex flex-col">
                  {msg.sender === 'ai' && <p className="text-primary text-base mb-1 px-6 text-left font-averia">Prometheus</p>}
                  <div
                    className={`rounded-lg px-6 py-3 ${
                      msg.sender === 'user'
                        ? 'w-full bg-primary text-foreground'
                        : 'w-fit max-w-[70%] bg-transparent text-foreground'
                    }`}
                  >
                    <div className={`text-sm ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
                      {msg.sender === 'ai' ? formatMessageContent(msg.content) : msg.content}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {/* Profiles Grid */}
            {profiles.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4 px-6">
                {profiles.map((profile) => (
                  <button
                    key={profile.id}
                    onClick={() => handleProfileClick(profile)}
                    className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted transition-all"
                  >
                    <div className="p-3 flex flex-col gap-0">
                      <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full h-[96px] mb-2 border-muted">
                        <img
                          alt={profile.name}
                          loading="lazy"
                          decoding="async"
                          src={profile.profilePictureUrl || '/default-avatar.svg'}
                          className="aspect-square size-full object-cover grayscale group-hover:grayscale-0 transition-all"
                        />
                      </span>
                      <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground group-hover:text-white">{profile.name}</h3>
                    </div>
                    <div className="p-3 pt-0">
                      <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground group-hover:text-white">
                        {profile.briefDescription}
                      </h4>
                      <p className="text-xs text-primary mt-2 text-left">Match Score: {profile.matchScore}%</p>
                    </div>
                  </button>
                ))}
              </div>
            )}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-lg px-6 py-3 max-w-[70%]">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-xs text-muted">Prometheus is typing...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="px-8 py-8">
            <MessageInput
              onSendMessage={sendMessage}
              disabled={isLoading}
            />
          </div>
        </div>
      </main>

      {/* Right-side Menu */}
      {selectedProfile && (
        <div className="fixed inset-y-0 right-0 w-[340px] bg-surface text-foreground transition-all z-50 animate-slide-in overflow-y-auto border-l border-muted">
          <div className="relative flex h-full flex-col">
            {/* Close button */}
            <div className="flex justify-end p-4">
              <button 
                onClick={() => setSelectedProfile(null)} 
                className="text-muted hover:text-foreground text-3xl leading-none transition-colors"
              >
                ×
              </button>
            </div>
            
            {/* Profile Section */}
            <div className="px-6 pb-6">
              {/* Profile Picture */}
              <div className="mb-6">
                <img 
                  src={selectedProfile.profilePictureUrl || '/default-avatar.svg'} 
                  alt={selectedProfile.name} 
                  className="w-32 h-32 object-cover bg-muted border-2 border-primary"
                />
              </div>
              
              {/* Action Buttons */}
              <div className="flex gap-3 mb-8">
                <button className="flex-1 bg-primary hover:brightness-95 text-foreground px-4 py-3 text-sm font-semibold transition-colors">
                  message
                </button>
                <button className="flex-1 bg-primary hover:brightness-95 text-foreground px-4 py-3 text-sm font-semibold transition-colors">
                  share
                </button>
              </div>
              
              {/* Download CV Button */}
              {selectedProfile.cvUrl && (
                <a 
                  href={selectedProfile.cvUrl}
                  download
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full bg-transparent border-2 border-primary hover:bg-primary text-primary hover:text-foreground px-4 py-3 text-sm font-semibold transition-colors flex items-center justify-center gap-2 mb-8"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download CV
                </a>
              )}
              
              {/* Name */}
              <h2 className="text-3xl font-bold mb-2">{selectedProfile.name}</h2>
              
              {/* Location */}
              <p className="text-muted text-sm mb-6">
                {selectedProfile.location || 'Location not specified'}
              </p>
              
              {/* TL;DR Section - Enhanced */}
              <div className="mb-8">
                <h3 className="text-foreground text-sm font-bold mb-3 uppercase tracking-wide">
                  TL;DR
                </h3>
                <div className="text-sm text-muted leading-relaxed space-y-2">
                  {selectedProfile.bio ? (
                    <p>{selectedProfile.bio}</p>
                  ) : selectedProfile.briefDescription ? (
                    <p>
                      {selectedProfile.name.split(' ')[0]} is a professional with expertise in {selectedProfile.briefDescription.toLowerCase()}. 
                      {selectedProfile.matchScore >= 80 && " They are an excellent match for your requirements with strong relevant experience."}
                      {selectedProfile.matchScore >= 60 && selectedProfile.matchScore < 80 && " They bring valuable skills and experience that align well with your needs."}
                      {selectedProfile.matchScore < 60 && " They have relevant experience that could be beneficial to your team."}
                    </p>
                  ) : (
                    <p>No description available</p>
                  )}
                </div>
              </div>
              
              {/* Today Section */}
              {selectedProfile.currentActivities && selectedProfile.currentActivities.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-foreground text-sm font-bold mb-3 uppercase tracking-wide">Current Focus</h3>
                  <ul className="space-y-2 text-muted text-sm">
                    {selectedProfile.currentActivities.map((activity, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>{activity}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {/* Projects Section */}
              {selectedProfile.projects && selectedProfile.projects.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-foreground text-sm font-bold mb-3 uppercase tracking-wide">Projects & Ventures</h3>
                  <ul className="space-y-2 text-muted text-sm">
                    {selectedProfile.projects.map((project, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>{project}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {/* Past Achievements Section */}
              {selectedProfile.achievements && selectedProfile.achievements.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-foreground text-sm font-bold mb-3 uppercase tracking-wide">Achievements</h3>
                  <ul className="space-y-2 text-muted text-sm">
                    {selectedProfile.achievements.map((achievement, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>{achievement}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {/* LinkedIn Link */}
              {selectedProfile.linkedinUrl && (
                <div className="mt-8 pt-6 border-t border-muted">
                  <a
                    href={selectedProfile.linkedinUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-primary hover:text-primary/80 text-sm font-semibold transition-colors"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                    View LinkedIn Profile
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}