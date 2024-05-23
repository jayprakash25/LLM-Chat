import React, { useEffect, useRef } from "react";

// Constants for chat types
const QUESTION_TYPE = "question";

export default function Chat({ chat: { type, text } }) {
  const endRef = useRef();

  // Scroll to the end of the chat when a new message is added
  useEffect(() => {
    endRef.current.scrollIntoView({ behavior: "smooth" });
  }, [text]);

  // Determine the direction of the chat based on the type
  const chatDirection =
    type === QUESTION_TYPE ? "flex-row-reverse" : "flex-row bg-gray-100";

  return (
    <div
      className={`flex py-4 px-2 rounded-lg space-x-2 md:space-x-4 w-full items-start font-semibold ${chatDirection}`}
    >
      {/* Chat text, with  styling for questions */}
      <div
        className={`w-[15.5rem] md:w-auto text-start md:max-w-lg lg:max-w-3xl ${
          type === QUESTION_TYPE && "bg-slate-200 px-4 py-2 rounded-lg"
        }`}
      >
        <p>{text}</p>
      </div>

      {/* Reference for scrolling to the end of the chat */}
      <div ref={endRef} />
    </div>
  );
}
