import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { getApiUrl, setApiUrl as storeApiUrl } from "./storage";
import { createApi, Api } from "./api";

interface ApiContextValue {
  apiUrl: string | null;
  api: Api | null;
  loading: boolean;
  setApiUrl: (url: string) => Promise<void>;
}

const ApiContext = createContext<ApiContextValue>({
  apiUrl: null,
  api: null,
  loading: true,
  setApiUrl: async () => {},
});

export function ApiProvider({ children }: { children: React.ReactNode }) {
  const [apiUrl, setUrl] = useState<string | null>(null);
  const [api, setApi] = useState<Api | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getApiUrl().then((url) => {
      if (url) {
        setUrl(url);
        setApi(createApi(url));
      }
      setLoading(false);
    });
  }, []);

  const setApiUrl = useCallback(async (url: string) => {
    const normalized = url.endsWith("/") ? url.slice(0, -1) : url;
    await storeApiUrl(normalized);
    setUrl(normalized);
    setApi(createApi(normalized));
  }, []);

  return (
    <ApiContext.Provider value={{ apiUrl, api, loading, setApiUrl }}>
      {children}
    </ApiContext.Provider>
  );
}

export function useApi() {
  return useContext(ApiContext);
}
