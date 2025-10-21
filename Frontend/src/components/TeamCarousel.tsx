import React from 'react';

interface TeamMember {
  name: string;
  image: string;
  description: string;
}

interface TeamCarouselProps {
  teamMembers: TeamMember[];
}

export default function TeamCarousel({ teamMembers }: TeamCarouselProps) {
  // Create 2 sets of team members for infinite scrolling (original + 1 duplicate)
  const carouselItems = [...teamMembers, ...teamMembers];

  return (
    <div className="relative h-64 w-full max-w-4xl mx-auto dashboard-carousel-container" role="region" aria-roledescription="carousel">
      <div className="dashboard-carousel">
        {carouselItems.map((member, index) => (
          <div
            key={`${member.name}-${index}`}
            role="group"
            aria-roledescription="slide"
            className="dashboard-carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]"
          >
            <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
              <div className="p-3 flex flex-col gap-0">
                <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                  <img
                    alt={member.name}
                    loading="lazy"
                    decoding="async"
                    src={member.image}
                    className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                  />
                </span>
                <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-white">
                  {member.name}
                </h3>
              </div>
              <div className="p-3 pt-0">
                <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-gray-500">
                  {member.description}
                </h4>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}