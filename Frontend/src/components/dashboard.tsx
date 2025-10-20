import TeamCarousel from './TeamCarousel';

export default function Dashboard() {
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
          <form>
                <div className="relative flex w-full grow flex-col justify-center overflow-hidden border border-muted bg-background">
                <textarea
                tabIndex={0}
                rows={1}
                placeholder="message prometheus..."
                spellCheck="false"
                className="w-full resize-none overflow-hidden bg-transparent py-3 pl-4 pr-10 outline-none placeholder:text-muted focus-within:outline-none text-foreground"

              />
              <div className="absolute right-2 z-10 flex items-center gap-1 sm:right-2">
              <button  className="relative inline-flex items-center justify-center rounded-md text-base font-semibold tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-none hover:bg-primary/90 size-8 p-0 hover:text-primary/50 text-foreground cursor-pointer" type="submit" data-state="closed"><svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" className="size-4"><path d="M8.14645 3.14645C8.34171 2.95118 8.65829 2.95118 8.85355 3.14645L12.8536 7.14645C13.0488 7.34171 13.0488 7.65829 12.8536 7.85355L8.85355 11.8536C8.65829 12.0488 8.34171 12.0488 8.14645 11.8536C7.95118 11.6583 7.95118 11.3417 8.14645 11.1464L11.2929 8H2.5C2.22386 8 2 7.77614 2 7.5C2 7.22386 2.22386 7 2.5 7H11.2929L8.14645 3.85355C7.95118 3.65829 7.95118 3.34171 8.14645 3.14645Z" fill="currentColor" fillRule="evenodd" clipRule="evenodd"></path></svg><span className="sr-only">what are you working on</span></button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
}