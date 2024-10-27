"use client";
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
import { Button } from "./ui/button";
import { Checkbox } from "./ui/checkbox";
// import { FormLabel, FormControl, FormItem } from "./ui/form";
import { useToast } from "../hooks/use-toast";

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
      });
    toast({
      variant: "destructive",
      title: "Request to save",
      description: "Saved successfully",
    })
    console.log(selectedTopics);
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
