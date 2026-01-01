export type Tag = {
  id: number;
  slug: string;
  label: string;
};

export type TagWithCount = Tag & {
  count: number;
};

export type WordExample = {
  id: number;
  sentence: string;
  source?: string | null;
};

export type Word = {
  id: number;
  term: string;
  meaning: string;
  notes?: string | null;
  freq: number;
  created_at: string;
  updated_at: string;
  examples: WordExample[];
  tags: Tag[];
};

export type WordList = {
  total: number;
  items: Word[];
};

export type WordSummary = {
  id: number;
  term: string;
  meaning: string;
};

export type TagDetail = {
  tag: Tag;
  total: number;
  words: WordSummary[];
};

export type SearchResponse = {
  total: number;
  items: Word[];
};
