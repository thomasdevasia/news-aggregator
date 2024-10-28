"use client";
import { Button } from "./ui/button";
import { useToast } from "../hooks/use-toast";
import { updateNewsSelection } from "@/lib/utils";

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("form submitted");
    // print selected topics
    const formData = new FormData(e.target);
    // console.log(topics);
    // for (let topic of topics) {
    //   console.log(topic.name, formData.get(topic.name));
    // }
    let selectedTopics = topics.filter((topic) => {
      return formData.get(topic.name) === "on";
    }).map((topic) => topic.name);
    console.log(selectedTopics);

    const sendTopics = async () => {
      const response = await updateNewsSelection(selectedTopics);
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
      // console.log(response);
      return response;
    }
    sendTopics();
    // console.log(sendTopics());


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
