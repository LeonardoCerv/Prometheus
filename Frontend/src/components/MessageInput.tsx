"use client";

import { useState } from "react";

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  placeholder?: string;
  disabled?: boolean;
}

export default function MessageInput({
  onSendMessage,
  placeholder = "message prometheus...",
  disabled = false
}: MessageInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || disabled) return;

    onSendMessage(message.trim());
    setMessage("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="relative flex w-full grow flex-col justify-center overflow-hidden border border-muted">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          tabIndex={0}
          rows={1}
          placeholder={placeholder}
          spellCheck="false"
          disabled={disabled}
          className="w-full resize-none overflow-hidden bg-transparent py-5 pl-8 pr-14 outline-none placeholder:text-muted focus-within:outline-none text-foreground disabled:opacity-50"
        />
        <div className="absolute right-4 z-10 flex items-center gap-1 sm:right-4">
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className="relative inline-flex items-center justify-center rounded-md text-base font-semibold tracking-base ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 shadow-none hover:bg-primary/90 size-8 p-0 hover:text-primary/50 text-foreground cursor-pointer disabled:cursor-not-allowed"
          >
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" className="size-4">
              <path d="M8.14645 3.14645C8.34171 2.95118 8.65829 2.95118 8.85355 3.14645L12.8536 7.14645C13.0488 7.34171 13.0488 7.65829 12.8536 7.85355L8.85355 11.8536C8.65829 12.0488 8.34171 12.0488 8.14645 11.8536C7.95118 11.6583 7.95118 11.3417 8.14645 11.1464L11.2929 8H2.5C2.22386 8 2 7.77614 2 7.5C2 7.22386 2.22386 7 2.5 7H11.2929L8.14645 3.85355C7.95118 3.65829 7.95118 3.34171 8.14645 3.14645Z" fill="currentColor" fillRule="evenodd" clipRule="evenodd"></path>
            </svg>
            <span className="sr-only">Send message</span>
          </button>
        </div>
      </div>
    </form>
  );
}