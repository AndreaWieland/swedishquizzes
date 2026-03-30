import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { useApi } from "@/lib/ApiContext";
import { ApiError } from "@/lib/api";
import { Topic, LearnStatus, LearnResponse } from "@/lib/types";
import TopicPicker from "@/components/TopicPicker";
import WordCard from "@/components/WordCard";

export default function LearnScreen() {
  const { api } = useApi();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [status, setStatus] = useState<LearnStatus | null>(null);
  const [currentWord, setCurrentWord] = useState<LearnResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingWord, setLoadingWord] = useState(false);
  const [allDone, setAllDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useFocusEffect(
    useCallback(() => {
      if (!api) return;
      setError(null);
      api.getTopics().then(setTopics).catch((e) => setError(e.message));
    }, [api])
  );

  useEffect(() => {
    if (!api || !selectedTopic) return;
    setLoading(true);
    setCurrentWord(null);
    setAllDone(false);
    setError(null);
    api
      .getLearnStatus(selectedTopic)
      .then((s) => {
        setStatus(s);
        if (s.remaining === 0) setAllDone(true);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [api, selectedTopic]);

  const learnNext = async () => {
    if (!api || !selectedTopic) return;
    setLoadingWord(true);
    setError(null);
    try {
      const word = await api.learnNext(selectedTopic);
      setCurrentWord(word);
      setStatus({
        topic: selectedTopic,
        learned: word.progress.learned,
        total: word.progress.total,
        remaining: word.progress.remaining,
      });
      if (word.progress.remaining === 0) setAllDone(true);
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) {
        setAllDone(true);
      } else {
        setError(e instanceof Error ? e.message : "Unknown error");
      }
    } finally {
      setLoadingWord(false);
    }
  };

  if (!api) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyText}>Please configure the API URL first.</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <TopicPicker
        topics={topics}
        selected={selectedTopic}
        onSelect={setSelectedTopic}
      />

      {error && (
        <View style={styles.errorCard}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      {loading && (
        <ActivityIndicator style={styles.loader} size="large" color="#2563eb" />
      )}

      {status && !loading && (
        <View style={styles.progressCard}>
          <Text style={styles.progressLabel}>Progress</Text>
          <Text style={styles.progressNumbers}>
            {status.learned} / {status.total} learned
          </Text>
          <View style={styles.progressBarBg}>
            <View
              style={[
                styles.progressBarFill,
                {
                  width: `${
                    status.total > 0
                      ? (status.learned / status.total) * 100
                      : 0
                  }%`,
                },
              ]}
            />
          </View>
        </View>
      )}

      {allDone && (
        <View style={styles.doneCard}>
          <Text style={styles.doneEmoji}>🎉</Text>
          <Text style={styles.doneTitle}>Congratulations!</Text>
          <Text style={styles.doneText}>
            You've learned all words in this topic. Head to the Quiz tab to test
            yourself!
          </Text>
        </View>
      )}

      {currentWord && !allDone && (
        <View style={styles.wordSection}>
          <WordCard data={currentWord} />
        </View>
      )}

      {selectedTopic && !loading && !allDone && (
        <TouchableOpacity
          style={[styles.learnButton, loadingWord && styles.buttonDisabled]}
          onPress={learnNext}
          disabled={loadingWord}
        >
          <Text style={styles.learnButtonText}>
            {loadingWord
              ? "Loading…"
              : currentWord
              ? "Next Word"
              : "Learn Next Word"}
          </Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f8f9fa",
  },
  emptyText: {
    fontSize: 16,
    color: "#64748b",
  },
  errorCard: {
    backgroundColor: "#fef2f2",
    borderRadius: 12,
    padding: 14,
    marginTop: 16,
  },
  errorText: {
    color: "#dc2626",
    fontSize: 14,
  },
  loader: {
    marginTop: 32,
  },
  progressCard: {
    backgroundColor: "#fff",
    borderRadius: 14,
    padding: 18,
    marginTop: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  progressLabel: {
    fontSize: 13,
    color: "#64748b",
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 6,
  },
  progressNumbers: {
    fontSize: 22,
    fontWeight: "700",
    color: "#1e293b",
    marginBottom: 12,
  },
  progressBarBg: {
    height: 8,
    backgroundColor: "#e2e8f0",
    borderRadius: 4,
    overflow: "hidden",
  },
  progressBarFill: {
    height: 8,
    backgroundColor: "#2563eb",
    borderRadius: 4,
  },
  doneCard: {
    backgroundColor: "#f0fdf4",
    borderRadius: 14,
    padding: 24,
    marginTop: 16,
    alignItems: "center",
  },
  doneEmoji: {
    fontSize: 40,
    marginBottom: 8,
  },
  doneTitle: {
    fontSize: 20,
    fontWeight: "700",
    color: "#16a34a",
    marginBottom: 8,
  },
  doneText: {
    fontSize: 15,
    color: "#475569",
    textAlign: "center",
    lineHeight: 22,
  },
  wordSection: {
    marginTop: 20,
  },
  learnButton: {
    backgroundColor: "#2563eb",
    borderRadius: 14,
    paddingVertical: 18,
    alignItems: "center",
    marginTop: 24,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  learnButtonText: {
    color: "#fff",
    fontSize: 17,
    fontWeight: "700",
  },
});
