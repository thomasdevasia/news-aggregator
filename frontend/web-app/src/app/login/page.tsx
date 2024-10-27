"use client";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { cookies } from "next/headers";
import { createUserAccount, loginUser } from "@/lib/utils";

export default function Login() {
  const router = useRouter();
  const handleSubmitCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    console.log("Create Account");
    console.log("Name: ", formData.get("name"));
    console.log("Username: ", formData.get("username"));
    console.log("Email: ", formData.get("email"));
    console.log("Password: ", formData.get("password"));
    let userData = {
      name: formData.get("name"),
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
    };
    // send the data to the server
    console.log("sending data to server");
   
    const data = await createUserAccount(userData);
    console.log("Data: ", data);

    // save the token in the local storage if the account is created successfully
    if (data.token) {
      document.cookie = `token=${data.token}`;
      console.log("Token saved in cookies");
      router.push("/home");
    }
  };

  const handleSubmitLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    console.log("Login");
    console.log("Username: ", formData.get("username"));
    console.log("Password: ", formData.get("password"));
    let userData = {
      username: formData.get("username"),
      password: formData.get("password"),
    };
    const data = await loginUser(userData);
    console.log("Data: ", data);

    if (data.token) {
      document.cookie = `token=${data.token}`;
      console.log("Token saved in cookies");
      router.push("/home");
    }
  };


  return (
    <div className="flex justify-center mt-5">
      <Tabs defaultValue="create_account" className="w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="create_account">Create Account</TabsTrigger>
          <TabsTrigger value="login">Login</TabsTrigger>
        </TabsList>
        <TabsContent value="create_account">
          <Card>
            <CardHeader>
              <CardTitle>Create Account</CardTitle>
              <CardDescription>
                Create an account to start using the app.
              </CardDescription>
            </CardHeader>
            <form onSubmit={handleSubmitCreate}>
              <CardContent className="space-y-2">
                <div className="space-y-1">
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" defaultValue="Your Name" name="name" />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="username">Username</Label>
                  <Input
                    id="username"
                    defaultValue="Username"
                    name="username"
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" defaultValue="abc@email.com" name="email" />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="Create_Password">Password</Label>
                  <Input id="Create_Password" type="password" name="password" />
                </div>
              </CardContent>
              <CardFooter>
                <Button type="submit">Create</Button>
              </CardFooter>
            </form>
          </Card>
        </TabsContent>
        <TabsContent value="login">
          <Card>
            <CardHeader>
              <CardTitle>Login</CardTitle>
              <CardDescription>
                Login to your account to start using the app.
              </CardDescription>
            </CardHeader>
            <form onSubmit={(e) => handleSubmitLogin(e)}>
              <CardContent className="space-y-2">
                <div className="space-y-1">
                  <Label htmlFor="Username">Username</Label>
                  <Input
                    id="Username"
                    defaultValue="Username"
                    name="username"
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="Password">Password</Label>
                  <Input id="Password" type="password" name="password" />
                </div>
              </CardContent>
              <CardFooter>
                <Button type="submit">Login</Button>
              </CardFooter>
            </form>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
