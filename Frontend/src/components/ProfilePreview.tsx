"use client";

import { ProfileData } from "@/app/be-found/page";

interface ProfilePreviewProps {
  profileData: ProfileData;
  email?: string;
  phone?: string;
}

export default function ProfilePreview({ profileData, email, phone }: ProfilePreviewProps) {
  const isEmpty = !profileData.personal_info.name;

  if (isEmpty) {
    return (
      <div className="max-w-4xl">
        <div className="p-12 bg-surface text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground mb-4 font-inter">
            no profile data yet
          </h2>
          <p className="text-lg text-muted">
            Start filling out your profile to see how it will look to recruiters.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl">
      {/* Profile Header Card */}
      <div className="shadow-md bg-surface mb-8">
        <div className="p-8">
          <div className="flex flex-col md:flex-row gap-6 items-start">
            {/* Profile Image */}
            <div className="relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted border-muted">
              {profileData.personal_info.image ? (
                <img
                  alt={profileData.personal_info.name || "Profile"}
                  src={profileData.personal_info.image}
                  className="aspect-square size-32 object-cover"
                />
              ) : (
                <div className="aspect-square size-32 flex items-center justify-center text-4xl font-bold text-foreground">
                  {profileData.personal_info.name ? profileData.personal_info.name.charAt(0).toUpperCase() : "?"}
                </div>
              )}
            </div>

            {/* Profile Info */}
            <div className="flex-1">
              <h1 className="text-4xl font-bold tracking-tight text-foreground mb-2 font-inter">
                {profileData.personal_info.name || "Your Name"}
              </h1>
              {profileData.personal_info.location && (
                <p className="text-base text-muted mb-2">📍 {profileData.personal_info.location}</p>
              )}
              {(email || phone) && (
                <div className="flex flex-col gap-1">
                  {email && (
                    <p className="text-base text-muted">✉️ {email}</p>
                  )}
                  {phone && (
                    <p className="text-base text-muted">📞 {phone}</p>
                  )}
                </div>
              )}
              <div className="mt-4">
                <button className="border border-primary text-primary px-4 py-2 hover:bg-primary hover:text-background transition-colors font-semibold">
                  view cv
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Skills Section */}
      {profileData.skills && (
        <div className="shadow-md bg-surface mb-8">
          <div className="p-6">
            <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4 font-inter">
              skills
            </h2>
            <p className="text-base leading-6 text-foreground">
              {profileData.skills}
            </p>
          </div>
        </div>
      )}

      {/* Job Experience Section */}
      {profileData.job_experience.length > 0 && (
        <div className="shadow-md bg-surface mb-8">
          <div className="p-6">
            <h2 className="text-2xl font-bold tracking-tight text-foreground mb-6 font-inter">
              job experience
            </h2>
            <div className="flex flex-col gap-6">
              {profileData.job_experience.map((exp, index) => (
                <div
                  key={index}
                  className="border-l-2 border-primary pl-4 hover:border-foreground transition-colors"
                >
                  <h3 className="text-xl font-bold text-foreground">
                    {exp.role || "Role"}
                  </h3>
                  <p className="text-lg text-primary font-semibold">
                    {exp.company || "Company"}
                  </p>
                  {(exp.start_date || exp.end_date) && (
                    <p className="text-sm text-muted mb-2">
                      {exp.start_date} {exp.start_date && exp.end_date && "- "} {exp.end_date}
                    </p>
                  )}
                  {exp.description && (
                    <p className="text-base text-foreground leading-6">
                      {exp.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Education Section */}
      {profileData.education.length > 0 && (
        <div className="shadow-md bg-surface mb-8">
          <div className="p-6">
            <h2 className="text-2xl font-bold tracking-tight text-foreground mb-6 font-inter">
              education
            </h2>
            <div className="flex flex-col gap-4">
              {profileData.education.map((edu, index) => (
                <div
                  key={index}
                  className="border border-muted p-4 bg-background hover:border-primary transition-colors"
                >
                  <h3 className="text-lg font-bold text-foreground">
                    {edu.degree || "Degree"}
                  </h3>
                  <p className="text-base text-primary font-semibold">
                    {edu.school || "School"}
                  </p>
                  {(edu.start_date || edu.end_date) && (
                    <p className="text-sm text-muted">
                      {edu.start_date} {edu.start_date && edu.end_date && "- "} {edu.end_date}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Projects Section */}
      {profileData.projects.length > 0 && (
        <div className="shadow-md bg-surface mb-8">
          <div className="p-6">
            <h2 className="text-2xl font-bold tracking-tight text-foreground mb-6 font-inter">
              projects
            </h2>
            <div className="flex flex-col gap-6">
              {profileData.projects.map((project, index) => (
                <div
                  key={index}
                  className="border border-muted p-4 bg-background hover:border-primary transition-colors"
                >
                  <h3 className="text-xl font-bold text-foreground mb-2">
                    {project.name || "Project Name"}
                  </h3>
                  {project.technologies && (
                    <p className="text-sm text-primary font-semibold mb-2">
                      {project.technologies}
                    </p>
                  )}
                  {project.description && (
                    <p className="text-base text-foreground leading-6 mb-3">
                      {project.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
