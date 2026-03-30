import {
  Topic,
  LearnStatus,
  LearnResponse,
  QuizQuestion,
  QuizAnswer,
  StatsResponse,
} from "./types";

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(baseUrl: string, path: string, options?: RequestInit): Promise<T> {
  const url = `${baseUrl}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {}
    throw new ApiError(res.status, detail);
  }

  return res.json();
}

export function createApi(baseUrl: string) {
  return {
    getTopics: () =>
      request<{ topics: Topic[] }>(baseUrl, "/topics").then((r) => r.topics),

    getLearnStatus: (topic: string) =>
      request<LearnStatus>(baseUrl, `/learn/status?topic=${encodeURIComponent(topic)}`),

    learnNext: (topic: string) =>
      request<LearnResponse>(baseUrl, `/learn?topic=${encodeURIComponent(topic)}`, {
        method: "POST",
      }),

    getQuiz: (topic: string) =>
      request<QuizQuestion>(baseUrl, `/quiz?topic=${encodeURIComponent(topic)}`),

    submitAnswer: (questionId: string, answer: string) =>
      request<QuizAnswer>(baseUrl, `/quiz/${encodeURIComponent(questionId)}`, {
        method: "POST",
        body: JSON.stringify({ answer }),
      }),

    getStats: () =>
      request<StatsResponse>(baseUrl, "/stats").then((r) => r.stats),
  };
}

export type Api = ReturnType<typeof createApi>;
