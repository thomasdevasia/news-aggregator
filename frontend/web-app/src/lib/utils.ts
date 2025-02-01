import { type ClassValue, clsx } from "clsx"
import { type } from "os"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const API_URL = "http://0.0.0.0:8000"
const API_URL_SERVER = "http://api-gateway:8000"

// create user createUserAccount
// typpe ofr formData in json
type signupDataType = {
  name: string
  username: string
  email: string
  password: string
}
export async function createUserAccount(formData: signupDataType) {
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

// updating news selection
// interface NewsSelection {
//   id: string
//   name: string
// }
export async function updateNewsSelection(topics: String[]) {

  let requestOptions = {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      topics: topics,
      action: "update",
    }),
  };
  // console.log(requestOptions)
  const response = await fetch(`${API_URL}/user/news_topic`, requestOptions);
  if (!response.ok) {
    return false;
  }
  else {
    const data = await response.json();
    return data;
  }
}

export async function getUserName(token: String | undefined) {
  let requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const response = await fetch(`${API_URL_SERVER}/user`, requestOptions);
  if (!response.ok) {
    return false;
  } else {
    const data = await response.json();
    return data;
  }
}

export async function getNewsSelection(token: String | null) {
  let requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const response = await fetch(`${API_URL}/user/news`, requestOptions);
  if (!response.ok) {
    return false;
  } else {
    const data = await response.json();
    return data;
  }
}

export async function getNews(token: String | null) {
  let requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    }
  };
  const response = await fetch(`${API_URL_SERVER}/user/news`, requestOptions);
  if (!response.ok) {
    return false;
  } else {
    const data = await response.json();
    return data;
  }
}
