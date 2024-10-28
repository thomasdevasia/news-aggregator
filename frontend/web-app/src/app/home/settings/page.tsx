import NewsSelection from "@/components/NewsSelection";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Settings() {
  return (
    <div className="flex flex-col">

      <Link href="/home/">
        <Button>Home</Button>
      </Link>
      <h1 className="text-3xl">Settings</h1>

      <div>
        <NewsSelection />
      </div>
    </div>
  );
}
