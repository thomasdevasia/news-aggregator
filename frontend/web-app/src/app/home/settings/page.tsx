import NewsSelection from "@/components/NewsSelection";

export default function Settings() {
  return (
    <div className="flex flex-col">
      <h1 className="text-3xl">Settings</h1>

      <div>
        <NewsSelection />
      </div>
    </div>
  );
}
