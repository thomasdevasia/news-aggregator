import newsData from "./newsData";
import express from "express";

const app = express();
const port = 3001;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Server is running');
});

const getFilteredNews = (newsTopics: String[]) => {
  const news = newsData.filter((newsItem) => {
    return newsTopics.includes(newsItem.type);
  });
  return news;
};
app.post('/getNews', (req, res) => {
  const newsTopics: String[] = req.body.topics;
  // console.log('Request for news topics: ', newsTopics);
  const news = getFilteredNews(newsTopics);
  // console.log('News sent: ', news);
  res.send(news);
});

app.listen(port, () => {
  console.log(`News collection service running at http://localhost:${port}`);
})
