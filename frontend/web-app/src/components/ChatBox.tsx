"use client";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

interface ChatMessage {
  id: number;
  message: string;
  user: string;
}

export default function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    // { id: 1, message: "Hello!", user: "User1" },
    // { id: 2, message: "Hi there!", user: "User2" },
    // { id: 3, message: "How are you?", user: "User1" },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  // const [userName, setUserName] = useState("");

  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
      // setMessages([...messages, newMsg]);
      const newMsg = {
        id: 0,
        message: newMessage,
        user: "Me",
      };
      setMessages((prev) => {
        newMsg.id = prev.length + 1;
        return [...prev, newMsg];
      });
      // console.log(messages);
      setNewMessage("");
      if (socket) {
        setIsStreaming(true);
        socket.send(JSON.stringify(newMsg));
      } else {
        // setMessages([...messages, newMsg]);
        setMessages((prev) => {
          const newMsg = {
            id: prev.length + 1,
            message: "Please connect to chat server",
            user: "AI",
          };
          return [...prev, newMsg];
        });
      }
    }
  };

  const [socket, setSocket] = useState<WebSocket | null>(null);
  const onClickConnect = () => {
    if (!socket) {
      // console.log("Connecting to server...");
      const userName = localStorage.getItem("username") as string;
      // TODO:change to api gate in future
      const WEB_SOCKET_URL = `ws://0.0.0.0:8002/${userName}/chat`;
      const socket = new WebSocket(WEB_SOCKET_URL);
      socket.onopen = () => {
        console.log("Connected to chat server");
      };
      socket.onmessage = (event) => {
        // console.log("Received message:", event.data);
        const resp = JSON.parse(event.data);
        if (resp.done) {
          setIsStreaming(false);
        } else {
          setMessages((prev) => {
            if (prev.length > 0 && prev[prev.length - 1].user === "AI") {
              const lastMsg = prev[prev.length - 1];
              const updatedMsg = {
                ...lastMsg,
                message: lastMsg.message + resp.response,
              };
              return [...prev.slice(0, prev.length - 1), updatedMsg];
            } else {
              return [
                ...prev,
                {
                  id: prev.length + 1,
                  message: resp.response,
                  user: "AI",
                },
              ];
            }
          });
        }
      };
      setSocket(socket);
    } else {
      // console.log("Disconnecting from server...");
      socket.close();
      setSocket(null);
    }
  };

  useEffect(() => {
    // setUserName(localStorage.getItem("username") as string);
    return () => {
      socket?.close();
    };
  }, [socket]);

  return (
    <div className="flex flex-col mt-4 h-[500px] w-[450px]">
      {/* Chat messages container */}
      <Button onClick={onClickConnect}>
        {socket ? "Disconnect" : "Connect"}
      </Button>
      <div className="flex-grow overflow-y-auto border-2 border-solid">
        <div className="flex flex-col space-y-2 p-4">
          {messages.map((msg, key) => (
            <p key={key} className="p-2 bg-gray-50 rounded">
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
          disabled={isStreaming}
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
