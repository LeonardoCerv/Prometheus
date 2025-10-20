"use client";

import { useState, useEffect } from "react";
import ProfileForm from "@/components/ProfileForm";
import ProfilePreview from "@/components/ProfilePreview";

export interface ProfileData {
  personal_info: {
    name: string;
    location: string;
    image: string;
  };
  education: Array<{
    degree: string;
    school: string;
    start_date: string;
    end_date: string;
  }>;
  job_experience: Array<{
    role: string;
    company: string;
    description: string;
    start_date: string;
    end_date: string;
  }>;
  projects: Array<{
    name: string;
    description: string;
    technologies: string;
  }>;
  skills: string;
}

export default function BeFoundPage() {
  const [showPreview, setShowPreview] = useState(false);
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [profileData, setProfileData] = useState<ProfileData>({
    personal_info: {
      name: "",
      location: "",
      image: "",
    },
    education: [],
    job_experience: [],
    projects: [],
    skills: "",
  });

  // Load parsed CV data and contact info from localStorage on mount
  useEffect(() => {
    const storedData = localStorage.getItem("profileData");
    const contactInfo = localStorage.getItem("contactInfo");
    
    if (contactInfo) {
      const { email: storedEmail, phone: storedPhone } = JSON.parse(contactInfo);
      setEmail(storedEmail || "");
      setPhone(storedPhone || "");
    }
    
    if (storedData) {
      const parsed = JSON.parse(storedData);
      
      // Sanitize data to ensure no null values for controlled inputs
      const sanitizedData: ProfileData = {
        personal_info: {
          name: parsed.personal_info?.name || "",
          location: parsed.personal_info?.location || "",
          image: parsed.personal_info?.image || "",
        },
        education: (parsed.education || []).map((edu: { degree?: string; school?: string; start_date?: string; end_date?: string }) => ({
          degree: edu?.degree || "",
          school: edu?.school || "",
          start_date: edu?.start_date || "",
          end_date: edu?.end_date || "",
        })),
        job_experience: (parsed.job_experience || []).map((exp: { role?: string; company?: string; description?: string; start_date?: string; end_date?: string }) => ({
          role: exp?.role || "",
          company: exp?.company || "",
          description: exp?.description || "",
          start_date: exp?.start_date || "",
          end_date: exp?.end_date || "",
        })),
        projects: (parsed.projects || []).map((proj: { name?: string; description?: string; technologies?: string }) => ({
          name: proj?.name || "",
          description: proj?.description || "",
          technologies: proj?.technologies || "",
        })),
        skills: parsed.skills || "",
      };
      
      setProfileData(sanitizedData);
      
      // Clear localStorage after loading
      localStorage.removeItem("profileData");
      localStorage.removeItem("contactInfo");
    }
  }, []);

  return (
    <main className="flex w-full flex-1 flex-col min-h-screen bg-background px-4 md:px-8 py-8">
      <div className="max-w-6xl mx-auto w-full">
        {/* Logo and Log Out */}
        <div className="flex justify-between items-center mb-8">
          <a href="/" className="flex items-center gap-4">
            <img src="/prometheus.svg" alt="Logo" width="64" height="64" />
            <p className="text-2xl font-medium leading-6 tracking-base text-foreground font-cormorant">
              <span className="text-primary text-2xl font-averia font-semibold">Prometheus</span>
            </p>
          </a>
          <button className="relative inline-flex items-center justify-center text-base font-semibold tracking-base shadow ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 border border-muted hover:bg-background/80 h-[42px] px-8 py-2 text-foreground">
            log out
          </button>
        </div>

        {/* Page Title and Preview Button */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tighter text-foreground font-inter mb-2">
              {showPreview ? "profile preview" : "edit your profile"}
            </h1>
            <p className="text-lg font-medium leading-6 tracking-base text-muted">
              {showPreview
                ? "This is how recruiters will see your profile"
                : "Update your information to stay discoverable"}
            </p>
          </div>
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="bg-transparent text-foreground relative inline-flex items-center border-2 border-primary justify-center text-primary text-base font-semibold tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-md hover:brightness-95 px-6 py-2"
          >
            {showPreview ? "edit profile" : "preview"}
          </button>
        </div>

        {/* Content */}
        {showPreview ? (
          <ProfilePreview profileData={profileData} email={email} phone={phone} />
        ) : (
          <ProfileForm
            profileData={profileData}
            setProfileData={setProfileData}
          />
        )}
      </div>
    </main>
  );
}
