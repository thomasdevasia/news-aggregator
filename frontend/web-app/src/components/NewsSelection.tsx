"use client";
import { Button } from "./ui/button";
import { useToast } from "../hooks/use-toast";
import { useEffect, useState } from "react";
import { updateNewsSelection, getNewsSelection } from "@/lib/utils";

const topics = [
  { id: "sports", name: "Sports" },
  { id: "politics", name: "Politics" },
  { id: "business", name: "Business" },
  { id: "entertainment", name: "Entertainment" },
  { id: "technology", name: "Technology" },
  { id: "health", name: "Health" },
  { id: "science", name: "Science" },
  { id: "world", name: "World" },
  { id: "local", name: "Local" },
  { id: "national", name: "National" },
  { id: "international", name: "International" },
  { id: "education", name: "Education" },
  { id: "lifestyle", name: "Lifestyle" },
];

export default function NewsSelection() {

  const { toast } = useToast();
  const [currentTopics, setCurrentTopics] = useState<string[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const fetchNewsSelection = async () => {
      const response = await getNewsSelection(token);
      console.log(response);
      if (response) {
        console.log(response.topics);
        setCurrentTopics(response.topics);
      }
    };
    fetchNewsSelection();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("form submitted");

    const sendTopics = async () => {
      const response = await updateNewsSelection(currentTopics);
      if (response) {
        toast({
          variant: "destructive",
          title: "Request to save",
          description: "Saved successfully",
        })
      }
      else {
        toast({
          variant: "destructive",
          title: "Request to save",
          description: "Failed to save",
        })
      }
      return response;
    }
    sendTopics();
  };

  const handleChange = (itemName: string) => {
    setCurrentTopics((prev) => {
      if (prev.includes(itemName)) {
        return prev.filter((topic) => topic !== itemName);
      } else {
        return [...prev, itemName];
      }
    });
  };

  return (
    <div className="flex flex-col ">
      <form action="" onSubmit={(e) => handleSubmit(e)}>
        {topics.map((topic) => (
          <div
            key={topic.id}
            className="flex align-middle items-center gap-y-3 "
          >
            <input
              type="checkbox"
              id={topic.id}
              name={topic.name}
              checked={currentTopics.includes(topic.name)}
              onChange={() => handleChange(topic.name)}
            />
            <label className="ml-2" htmlFor={topic.id}>{topic.name}</label>
          </div>
        ))}
        <Button type="submit" className="mt-3">
          Save
        </Button>
      </form>
    </div>
  );
}
