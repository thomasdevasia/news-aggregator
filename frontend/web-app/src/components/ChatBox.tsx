"use client";
import { useState } from "react";

interface ChatMessage {
  id: number;
  message: string;
  user: string;
}

export default function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: 1, message: "Hello!", user: "User1" },
    { id: 2, message: "Hi there!", user: "User2" },
    { id: 3, message: "How are you?", user: "User1" },
  ]);
  const [newMessage, setNewMessage] = useState("");

  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
      const newMsg = {
        id: messages.length + 1,
        message: newMessage,
        user: "User1",
      };
      setMessages([...messages, newMsg]);
      setNewMessage("");
    }
  };

  return (
    <div className="flex flex-col mt-4 h-[500px] w-[450px]">
      {/* Chat messages container */}
      <div className="flex-grow overflow-y-auto border-2 border-solid">
        <div className="flex flex-col space-y-2 p-4">
          {messages.map((msg) => (
            <p key={msg.id} className="p-2 bg-gray-50 rounded">
              <strong>{msg.user}:</strong> {msg.message}
            </p>
          ))}
        </div>
      </div>
      {/* Input box and send button */}
      <div className="flex w-full p-2 ">
        <input
          type="text"
          className="flex-grow p-2 border border-gray-300 rounded"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSendMessage();
            }
          }}
          placeholder="Type your message..."
        />
        <button
          className="ml-2 p-2 bg-slate-500 text-white rounded"
          onClick={handleSendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
