export interface TopicCounts {
  nouns: number;
  verbs: number;
  misc: number;
  total: number;
}

export interface Topic {
  name: string;
  display_name: string;
  counts: TopicCounts;
}

export interface LearnStatus {
  topic: string;
  learned: number;
  total: number;
  remaining: number;
}

export interface NounWord {
  indefinite: string;
  definite: string;
  plural: string;
  plural_definite: string;
  english: string;
  cefr: number;
  frequency: number;
}

export interface VerbWord {
  infinitive: string;
  present: string;
  past: string;
  supine: string;
  imperative?: string;
  english: string;
  cefr: number;
  frequency: number;
}

export interface MiscWord {
  swedish: string;
  english: string;
  cefr: number;
  frequency: number;
}

export type WordData = NounWord | VerbWord | MiscWord;

export interface LearnResponse {
  topic: string;
  type: "noun" | "verb" | "misc";
  word_key: string;
  word: WordData;
  progress: {
    learned: number;
    total: number;
    remaining: number;
  };
}

export interface QuizQuestion {
  type: "noun" | "verb" | "misc";
  form: string;
  direction: string;
  word: WordData;
  prompt: string;
  options?: string[];
  question_id: string;
}

export interface QuizAnswer {
  correct: boolean;
  correct_answer: string;
  stats: {
    asked: number;
    correct: number;
  };
}

export interface TopicStats {
  total_asked: number;
  total_correct: number;
  accuracy: number;
  words_seen: number;
}

export interface StatsResponse {
  stats: Record<string, TopicStats>;
}
