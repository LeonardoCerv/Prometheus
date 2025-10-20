export default function Sidebar() {
  return (
    <div className="fixed inset-y-0 hidden w-[290px] border-r border-dashed bg-surface py-6 pl-6 transition-all md:block border-muted">
      <div className="relative flex h-full flex-col gap-2">
        <a className="pl-2" href="/">
          <div className="flex w-full items-center">
            <img src="/prometheus.svg" alt="Logo" width="64" height="64" />
          </div>
        </a>
        <div className="text-muted flex w-full flex-col gap-0 pt-4 md:pr-6 text-sm text-foreground">
          <a href="/">
            <button className="relative inline-flex items-center justify-center rounded-md font-semibold tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 text-base leading-none text-foreground hover:text-primary px-0 py-2 h-auto">discover</button>
          </a>
          <div className="my-3 w-full border-b border-dashed border-muted"></div>
          <p className="text-base font-medium leading-6 tracking-base pr-6 text-foreground pb-6">
            welcome to <span className="text-primary text-xl font-cormorant font-semibold">Prometheus</span>.
          </p>
          <p className="text-base font-medium leading-6 tracking-base pr-6 text-muted pb-4">
            <span className="text-primary text-xl font-cormorant font-semibold">Find</span> the perfect fit for a role. Get rid of the struggle of reviewing hundreds of applicants.
          </p>
          <p className="text-base font-medium leading-6 tracking-base pr-6 text-muted pb-4">
            <span className="text-primary text-xl font-cormorant font-semibold">Be found</span> without applying. Build your profile once and let opportunities come to you.
          </p>
        </div>
        <div className="mt-auto flex flex-col gap-3 pr-6">
          <button className="bg-primary text-foreground relative inline-flex items-center justify-center text-base font-semibold tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-md hover:brightness-95 h-[42px] px-4 py-2">
            sign up
          </button>
          <button className="relative inline-flex items-center justify-center text-base font-semibold tracking-base shadow ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 border border-muted hover:bg-background/80 h-[42px] px-4 py-2 text-foreground">
            log in
          </button>
        </div>
      </div>
    </div>
  );
}