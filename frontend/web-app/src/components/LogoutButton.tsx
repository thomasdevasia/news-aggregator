"use client";
import { Button } from "./ui/button";
import { useRouter } from "next/navigation";

const LogoutButton = () => {
  const router = useRouter();
  const handleLogout = () => {
    console.log("Logout");
    // remove token from cookies
    document.cookie = `token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    console.log("Token removed from cookies");
    router.push("/");
  };
  return (
    <Button type="submit" onClick={handleLogout}>
      Logout
    </Button>
  );
};

export default LogoutButton;
