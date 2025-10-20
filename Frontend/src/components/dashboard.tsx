import TeamCarousel from './TeamCarousel';
import MessageInput from './MessageInput';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();

  const teamMembers = [
    {
      name: 'Kike',
      image: '/kike.jpeg',
      description: 'Team Member'
    },
    {
      name: 'Leo',
      image: '/leo.jpg',
      description: 'Team Member'
    },
    {
      name: 'Ian',
      image: '/Ian.jpg',
      description: 'Team Member'
    },
    {
      name: 'Mateo',
      image: '/mateo.jpeg',
      description: 'Team Member'
    },
    {
      name: 'Jhon',
      image: '/jhon.jpg',
      description: 'Team Member'
    }
  ];

  const handleSendMessage = (message: string) => {
    // Create new conversation
    const newConversation = {
      id: Date.now().toString(),
      title: message.length > 50 ? message.substring(0, 50) + '...' : message,
      timestamp: new Date(),
      type: 'job_search' as const,
      messages: [{
        id: Date.now().toString(),
        content: message,
        sender: 'user' as const,
        timestamp: new Date()
      }]
    };

    // Get existing conversations
    const existingConversations = JSON.parse(localStorage.getItem('conversations') || '[]');

    // Add new conversation to the beginning
    const updatedConversations = [newConversation, ...existingConversations];

    // Save to localStorage
    localStorage.setItem('conversations', JSON.stringify(updatedConversations));

    // Navigate to the new chat
    router.push(`/chat/${newConversation.id}`);
  };

  const handleButtonClick = (buttonText: string) => {
    // Create new conversation with button text as message
    const newConversation = {
      id: Date.now().toString(),
      title: buttonText.length > 50 ? buttonText.substring(0, 50) + '...' : buttonText,
      timestamp: new Date(),
      type: 'job_search' as const,
      messages: [{
        id: Date.now().toString(),
        content: buttonText,
        sender: 'user' as const,
        timestamp: new Date()
      }]
    };

    // Get existing conversations
    const existingConversations = JSON.parse(localStorage.getItem('conversations') || '[]');

    // Add new conversation to the beginning
    const updatedConversations = [newConversation, ...existingConversations];

    // Save to localStorage
    localStorage.setItem('conversations', JSON.stringify(updatedConversations));

    // Navigate to the new chat
    router.push(`/chat/${newConversation.id}`);
  };
  return (
    <main className="flex w-full flex-1 flex-col md:pl-[272px] lg:pr-0">
      <div className="pt-8 h-[calc(100dvh-7px)] flex flex-col gap-16">
        <div className="my-18 mx-auto flex flex-col gap-16">
          <h1 className="text-5xl font-extrabold tracking-tighter sm:text-6xl text-center text-foreground font-inter">
            find and<br />be found.
          </h1>
          <div className="flex flex-col gap-4">
            {/* Team Carousel */}
            <TeamCarousel teamMembers={teamMembers} />

            {/* Carousel for top-Buttons */}
            <div className="relative button-carousel-container" role="region" aria-roledescription="carousel">
              <div className="gap-4 top-button-carousel">
                  <button onClick={() => handleButtonClick("looking for a marketer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button onClick={() => handleButtonClick("show me hardware people")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button onClick={() => handleButtonClick("need a producer for my album")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button onClick={() => handleButtonClick("i need to hire a react engineer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button onClick={() => handleButtonClick("show me content creators")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button onClick={() => handleButtonClick("experts on tiktok")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
                  <button onClick={() => handleButtonClick("who are some people i should invest in?")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">who are some people i should invest in?</button>
                  <button onClick={() => handleButtonClick("tell me the legend of naveed")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">tell me the legend of naveed</button>
                  <button onClick={() => handleButtonClick("i'm building in gaming")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">i'm building in gaming</button>
                  <button onClick={() => handleButtonClick("show me fast growing projects")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-1 py-1 text-foreground hover:text-primary border-muted">show me fast growing projects</button>
                  {/* Duplicate buttons for infinite loop */}
                  <button onClick={() => handleButtonClick("looking for a marketer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button onClick={() => handleButtonClick("show me hardware people")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button onClick={() => handleButtonClick("need a producer for my album")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button onClick={() => handleButtonClick("i need to hire a react engineer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button onClick={() => handleButtonClick("show me content creators")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button onClick={() => handleButtonClick("experts on tiktok")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
              </div>
            </div>
            {/* Carousel for bottom-Buttons */}
              <div className="relative button-carousel-container" role="region" aria-roledescription="carousel">
              <div className="gap-4 bottom-button-carousel">
                  <button onClick={() => handleButtonClick("looking for a marketer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button onClick={() => handleButtonClick("show me hardware people")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button onClick={() => handleButtonClick("need a producer for my album")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button onClick={() => handleButtonClick("i need to hire a react engineer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button onClick={() => handleButtonClick("show me content creators")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button onClick={() => handleButtonClick("experts on tiktok")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
                  <button onClick={() => handleButtonClick("who are some people i should invest in?")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">who are some people i should invest in?</button>
                  <button onClick={() => handleButtonClick("tell me the legend of naveed")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">tell me the legend of naveed</button>
                  <button onClick={() => handleButtonClick("i'm building in gaming")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">i'm building in gaming</button>
                  <button onClick={() => handleButtonClick("show me fast growing projects")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-1 py-1 text-foreground hover:text-primary border-muted">show me fast growing projects</button>
                  {/* Duplicate buttons for infinite loop */}
                  <button onClick={() => handleButtonClick("looking for a marketer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button onClick={() => handleButtonClick("show me hardware people")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button onClick={() => handleButtonClick("need a producer for my album")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button onClick={() => handleButtonClick("i need to hire a react engineer")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button onClick={() => handleButtonClick("show me content creators")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button onClick={() => handleButtonClick("experts on tiktok")} className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
              </div>
            </div>
            {/* Carousel for bottom-Buttons */}
              <div className="relative button-carousel-container" role="region" aria-roledescription="carousel">
              <div className="gap-4 bottom-button-carousel">
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">who are some people i should invest in?</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">tell me the legend of naveed</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">i'm building in gaming</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-1 py-1 text-foreground hover:text-primary border-muted">show me fast growing projects</button>
                  {/* Duplicate buttons for infinite loop */}
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">looking for a marketer</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me hardware people</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">need a producer for my album</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border border-muted px-4 py-1 text-foreground hover:text-primary border-muted">i need to hire a react engineer</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">show me content creators</button>
                  <button className="button-item hover:text-white h-10 flex-shrink-0 cursor-pointer border px-4 py-1 text-foreground hover:text-primary border-muted">experts on tiktok</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="sticky mt-auto md:max-w-xl bottom-0 mx-auto w-full bg-background/70 backdrop-blur-md">
        <div className="flex flex-col gap-4 border-t py-4 md:border-none px-4 md:px-0 md:py-6">
          <MessageInput onSendMessage={handleSendMessage} />
        </div>
      </div>
    </main>
  );
}