export default function Landing() {
  return (
    <main className="flex w-full flex-1 flex-col h-screen">
      <div className="flex flex-col justify-between h-full pt-8 pb-8">
        {/* Header with Logo on left and Login button on right */}
        <div className="flex justify-between items-center px-4 md:px-8">
          <a href="/" className="flex items-center gap-4">
            <img src="/prometheus.svg" alt="Logo" width="72" height="72" />
            <p className="text-3xl font-medium leading-6 tracking-base text-foreground font-cormorant">
              <span className="text-primary text-3xl font-averia font-semibold">Prometheus</span>
            </p>
          </a>
          <button className="relative inline-flex items-center justify-center text-base font-semibold tracking-base shadow ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 border border-muted hover:bg-background/80 h-[42px] px-8 py-2 text-foreground">
            log in
          </button>
        </div>

        <h1 className="-mt-32 text-7xl font-extrabold tracking-tighter sm:text-8xl text-center text-foreground font-inter">
          find and<br />be found.
        </h1>

        {/* Find and Be Found Description - Moved up */}
        <div className="-mt-16 flex flex-col px-4 md:px-0">
          <div className="flex flex-col md:flex-row justify-center md:justify-evenly w-full">
            {/* Employers/Recruiters Column */}
            <div className="flex flex-col gap-4 md:max-w-sm">
              <a href="/find/sign-up">
                <button className="bg-transparent text-foreground relative inline-flex items-center border-2 border-primary justify-center text-primary  text-3xl tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-md hover:brightness-95 px-4 py-2 font-fjalla">
                  Find
                </button>
              </a>
              <div>
                <p className="text-lg font-medium leading-6 tracking-base pr-6 text-muted pb-4">
                  <span className="text-primary">Find the perfect fit for a role. </span> 
                  Get rid of the struggle of reviewing hundreds of applicants.
                </p>
              </div>
            </div>

            {/* Applicants/Professionals Column */}
            <div className="flex flex-col gap-4 md:max-w-sm">
              <a href="/register">
                <button className="bg-transparent text-foreground relative inline-flex items-center border-2 border-primary justify-center text-primary  text-3xl tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-md hover:brightness-95 px-4 py-2 font-fjalla w-full">
                  Be Found
                </button>
              </a>
              <div>
                <p className="text-lg font-medium leading-6 tracking-base pr-6 text-muted pb-4">
                  <span className="text-primary">Be found without applying. </span>
                   Fill your profile once and let opportunities come to you.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="-mt-16 flex flex-col gap-4">
          {/* Carousel for People */}
          <div className="relative h-64 w-full max-w-5xl mx-auto overflow-hidden" role="region" aria-roledescription="carousel">
            <div className="carousel gap-4">
          <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
            <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Kike"
                        loading="lazy"
                        decoding="async"
                        src="/kike.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Kike</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Mateo"
                        loading="lazy"
                        decoding="async"
                        src="/mateo.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Mateo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Ian"
                        loading="lazy"
                        decoding="async"
                        src="/Ian.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Ian</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Leo"
                        loading="lazy"
                        decoding="async"
                        src="/leo.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Leo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
                            <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Jhon"
                        loading="lazy"
                        decoding="async"
                        src="/jhon.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Jhon</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              {/* uplicate cards for infinite loop */}
          <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
            <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Kike"
                        loading="lazy"
                        decoding="async"
                        src="/kike.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Kike</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Mateo"
                        loading="lazy"
                        decoding="async"
                        src="/mateo.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Mateo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Ian"
                        loading="lazy"
                        decoding="async"
                        src="/Ian.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Ian</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Leo"
                        loading="lazy"
                        decoding="async"
                        src="/leo.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Leo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
                            <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Jhon"
                        loading="lazy"
                        decoding="async"
                        src="/jhon.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Jhon</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              {/* Second Duplicate cards for infinite loop */}
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Kike"
                        loading="lazy"
                        decoding="async"
                        src="/kike.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Kike</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Mateo"
                        loading="lazy"
                        decoding="async"
                        src="/mateo.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Mateo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Ian"
                        loading="lazy"
                        decoding="async"
                        src="/Ian.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Ian</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Leo"
                        loading="lazy"
                        decoding="async"
                        src="/leo.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Leo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              {/* Third set of cards for infinite loop */}
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Kike"
                        loading="lazy"
                        decoding="async"
                        src="/kike.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Kike</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Mateo"
                        loading="lazy"
                        decoding="async"
                        src="/mateo.jpeg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Mateo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Ian"
                        loading="lazy"
                        decoding="async"
                        src="/Ian.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Ian</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Jhon"
                        loading="lazy"
                        decoding="async"
                        src="/jhon.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Jhon</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
              <div role="group" aria-roledescription="slide" className="carousel-item shrink-0 grow-0 basis-full pl-6 max-w-[200px]">
                <div className="border text-foreground shadow-md group hover:text-white h-64 bg-transparent cursor-pointer opacity-80 hover:opacity-100 border-muted">
                  <div className="p-3 flex flex-col gap-0">
                    <span className="group relative flex shrink-0 items-center justify-center overflow-hidden border bg-muted size-14 w-full min-hover:text-white h-[96px] mb-2 border-muted">
                      <img
                        alt="Leo"
                        loading="lazy"
                        decoding="async"
                        src="/leo.jpg"
                        className="aspect-square size-full object-cover grayscale group-hover:grayscale-0"
                      />
                    </span>
                    <h3 className="tracking-tight line-clamp-1 text-left font-medium text-lg lg:text-lg text-foreground">Leo</h3>
                  </div>
                  <div className="p-3 pt-0">
                    <h4 className="font-semibold tracking-tight line-clamp-3 truncate whitespace-break-spaces text-sm pb-0 text-left text-foreground">
                      Team Member
                    </h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}