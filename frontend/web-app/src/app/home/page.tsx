import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col gap-y-4">
      <h1 className="text-3xl">Home</h1>
      <Link href="/home/settings">
        <Button> Settings </Button>
      </Link>
    </div>
  );
}
