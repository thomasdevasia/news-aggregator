import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-4 p-24">
      <h1 className="text-4xl font-bold">Welcome to the Web App</h1>

      <Link href="/login">
        <Button type="submit">Go to Login</Button>
      </Link>
      <Link href="/home">
        <Button type="submit">Go to Home</Button>
      </Link>
    </main>
  );
}
