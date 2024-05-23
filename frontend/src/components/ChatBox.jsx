import React, { useState } from "react";
import axios from "axios";
import Chat from "./Chat";
import TextField from "./TextField";

// Constants for chat types
const QUESTION_TYPE = "question";
const ANSWER_TYPE = "answer";

export default function ChatBox() {
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async (question) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        content: question,
      });

      console.log(response.data);

      // Adding the question and answer to the chat history
      setChatHistory([
        ...chatHistory,
        { text: question, type: QUESTION_TYPE },
        { text: response.data.response, type: ANSWER_TYPE },
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div className="px-8 md:px-20 lg:px-36 py-32 ">
        {chatHistory.map((chat, index) => (
          <Chat key={index} chat={chat} />
        ))}
      </div>
      <TextField handleSend={handleSend} />
    </div>
  );
}
