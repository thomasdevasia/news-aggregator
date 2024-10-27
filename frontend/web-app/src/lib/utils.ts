import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const API_URL = "http://0.0.0.0:8000"

// create user createUserAccount
// typpe ofr formData in json
type signupDataType = {
  name: string
  username: string
  email: string
  password: string
}
export async function createUserAccount(formData : signupDataType) {
  const response = await fetch(`${API_URL}/signup`, {
    method: "POST",
    body: JSON.stringify({
      name: formData["name"],
      username: formData["username"],
      email: formData["email"],
      password: formData["password"],
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  const data = await response.json();
  return data;
}

// login to user account
type loginDataType = {
  username: string
  password: string
}

export async function loginUser(formData: loginDataType) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      Authorization: `Basic ${btoa(`${formData["username"]}:${formData["password"]}`)}`,
    },
  });
  const data = await response.json();
  return data;
}
