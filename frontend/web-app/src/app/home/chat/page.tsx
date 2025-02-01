import Link from "next/link";
import { Button } from "@/components/ui/button";
import ChatBox from "@/components/ChatBox";

export default function Settings() {
  return (
    <div className="flex flex-col">

      <Link href="/home/">
        <Button>Home</Button>
      </Link>
      <h1 className="text-3xl">Chat</h1>
      <ChatBox />

    </div>
  );
}
