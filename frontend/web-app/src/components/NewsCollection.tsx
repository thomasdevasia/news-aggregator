import { getNews } from "@/lib/utils";
import { cookies } from "next/headers";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
  CardDescription,
} from "@/components/ui/card";

interface NewsType {
  news_id: number;
  heading: string;
  data: string;
  newsType: string;
  source: string;
  dateCreated: string;
}

export default async function NewsCollection() {
  const token: string = cookies().get("token")?.value as string;
  console.log(token);
  const response = await getNews(token);
  const allNews: NewsType[] = response.allNews;
  // console.log(allNews);
  return (
    <div>
      <h1 className="text-2xl">News Collection</h1>
      {allNews.map((news: NewsType) => (
        <div key={news.news_id} className="m-4">
          <Card>
            <CardHeader>
              <CardTitle>{news.heading}</CardTitle>
              <CardDescription>{news.source}</CardDescription>
            </CardHeader>
            <CardContent>
              <p>{news.data}</p>
            </CardContent>
            <CardFooter>
              <p>{news.dateCreated}</p>
            </CardFooter>
          </Card>
        </div>
      ))}
    </div>
  );
}
