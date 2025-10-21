export interface ProfessionalProfile {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  profession: string;
  bio: string;
  experience: number; // years of experience
  skills: string[];
  education: {
    degree: string;
    institution: string;
    year: number;
  }[];
  location: string;
  profileImage?: string;
  portfolioUrl?: string;
  linkedinUrl?: string;
  isProfileComplete: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ProfessionalFormData extends Omit<ProfessionalProfile, 'id' | 'createdAt' | 'updatedAt' | 'isProfileComplete'> {
  // This interface can be used for form handling
}
