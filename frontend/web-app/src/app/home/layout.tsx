import LogoutButton from "@/components/LogoutButton";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/toaster"
import UserName from "@/components/UserName";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col items-center gap-4 p-24">
      <h1 className="text-4xl font-bold">News-Aggregator</h1>
      <LogoutButton />
      <UserName />
      <main>{children}</main>
      <Toaster />
    </div>
  );
}
