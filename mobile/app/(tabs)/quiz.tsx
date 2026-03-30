import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { useApi } from "@/lib/ApiContext";
import { ApiError } from "@/lib/api";
import { Topic, QuizQuestion, QuizAnswer } from "@/lib/types";
import TopicPicker from "@/components/TopicPicker";

export default function QuizScreen() {
  const { api } = useApi();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [question, setQuestion] = useState<QuizQuestion | null>(null);
  const [answer, setAnswer] = useState<QuizAnswer | null>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [freeText, setFreeText] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [noWords, setNoWords] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useFocusEffect(
    useCallback(() => {
      if (!api) return;
      api.getTopics().then(setTopics).catch((e) => setError(e.message));
    }, [api])
  );

  const fetchQuestion = useCallback(async () => {
    if (!api || !selectedTopic) return;
    setLoading(true);
    setQuestion(null);
    setAnswer(null);
    setSelectedOption(null);
    setFreeText("");
    setNoWords(false);
    setError(null);
    try {
      const q = await api.getQuiz(selectedTopic);
      setQuestion(q);
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) {
        setNoWords(true);
      } else {
        setError(e instanceof Error ? e.message : "Unknown error");
      }
    } finally {
      setLoading(false);
    }
  }, [api, selectedTopic]);

  useEffect(() => {
    fetchQuestion();
  }, [fetchQuestion]);

  const submitAnswer = async (value: string) => {
    if (!api || !question || submitting) return;
    setSubmitting(true);
    setError(null);
    try {
      const result = await api.submitAnswer(question.question_id, value);
      setAnswer(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleOptionPress = (option: string) => {
    if (answer) return;
    setSelectedOption(option);
    submitAnswer(option);
  };

  const handleFreeTextSubmit = () => {
    if (!freeText.trim()) return;
    submitAnswer(freeText.trim());
  };

  if (!api) {
    return (
      <View style={styles.center}>
        <Text style={styles.emptyText}>Please configure the API URL first.</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
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

      {noWords && (
        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>No learned words yet</Text>
          <Text style={styles.infoText}>
            Go to the Learn tab first to learn some words before taking a quiz!
          </Text>
        </View>
      )}

      {question && !loading && (
        <View style={styles.questionCard}>
          <Text style={styles.questionPrompt}>{question.prompt}</Text>

          {question.options ? (
            <View style={styles.optionsContainer}>
              {question.options.map((option, i) => {
                let optionStyle = styles.option;
                let textStyle = styles.optionText;

                if (answer) {
                  if (option === answer.correct_answer) {
                    optionStyle = { ...styles.option, ...styles.optionCorrect };
                    textStyle = { ...styles.optionText, ...styles.optionTextCorrect };
                  } else if (
                    option === selectedOption &&
                    !answer.correct
                  ) {
                    optionStyle = { ...styles.option, ...styles.optionWrong };
                    textStyle = { ...styles.optionText, ...styles.optionTextWrong };
                  }
                } else if (option === selectedOption) {
                  optionStyle = { ...styles.option, ...styles.optionSelected };
                }

                return (
                  <TouchableOpacity
                    key={i}
                    style={optionStyle}
                    onPress={() => handleOptionPress(option)}
                    disabled={!!answer || submitting}
                  >
                    <Text style={textStyle}>{option}</Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          ) : (
            <View style={styles.freeTextContainer}>
              <TextInput
                style={styles.freeInput}
                value={freeText}
                onChangeText={setFreeText}
                placeholder="Type your answer…"
                placeholderTextColor="#94a3b8"
                editable={!answer}
                autoCapitalize="none"
                autoCorrect={false}
                onSubmitEditing={handleFreeTextSubmit}
                returnKeyType="done"
              />
              {!answer && (
                <TouchableOpacity
                  style={[
                    styles.submitButton,
                    submitting && styles.buttonDisabled,
                  ]}
                  onPress={handleFreeTextSubmit}
                  disabled={submitting || !freeText.trim()}
                >
                  <Text style={styles.submitButtonText}>
                    {submitting ? "…" : "Submit"}
                  </Text>
                </TouchableOpacity>
              )}
            </View>
          )}

          {answer && (
            <View
              style={[
                styles.resultCard,
                answer.correct ? styles.resultCorrect : styles.resultWrong,
              ]}
            >
              <Text style={styles.resultTitle}>
                {answer.correct ? "Correct!" : "Incorrect"}
              </Text>
              {!answer.correct && (
                <Text style={styles.resultAnswer}>
                  Correct answer: {answer.correct_answer}
                </Text>
              )}
              <Text style={styles.resultStats}>
                Accuracy: {answer.stats.correct}/{answer.stats.asked}
              </Text>
            </View>
          )}

          {answer && (
            <TouchableOpacity style={styles.nextButton} onPress={fetchQuestion}>
              <Text style={styles.nextButtonText}>Next Question</Text>
            </TouchableOpacity>
          )}
        </View>
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
  infoCard: {
    backgroundColor: "#eff6ff",
    borderRadius: 14,
    padding: 24,
    marginTop: 24,
    alignItems: "center",
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#2563eb",
    marginBottom: 8,
  },
  infoText: {
    fontSize: 15,
    color: "#475569",
    textAlign: "center",
    lineHeight: 22,
  },
  questionCard: {
    marginTop: 20,
  },
  questionPrompt: {
    fontSize: 20,
    fontWeight: "700",
    color: "#1e293b",
    lineHeight: 28,
    marginBottom: 20,
    textAlign: "center",
  },
  optionsContainer: {
    gap: 10,
  },
  option: {
    backgroundColor: "#fff",
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 20,
    borderWidth: 2,
    borderColor: "#e2e8f0",
  },
  optionSelected: {
    borderColor: "#2563eb",
    backgroundColor: "#eff6ff",
  },
  optionCorrect: {
    borderColor: "#16a34a",
    backgroundColor: "#f0fdf4",
  },
  optionWrong: {
    borderColor: "#dc2626",
    backgroundColor: "#fef2f2",
  },
  optionText: {
    fontSize: 16,
    color: "#1e293b",
    textAlign: "center",
  },
  optionTextCorrect: {
    color: "#16a34a",
    fontWeight: "600",
  },
  optionTextWrong: {
    color: "#dc2626",
    fontWeight: "600",
  },
  freeTextContainer: {
    gap: 12,
  },
  freeInput: {
    backgroundColor: "#fff",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    borderWidth: 1,
    borderColor: "#e2e8f0",
    color: "#1e293b",
  },
  submitButton: {
    backgroundColor: "#2563eb",
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  submitButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  resultCard: {
    borderRadius: 14,
    padding: 18,
    marginTop: 20,
    alignItems: "center",
  },
  resultCorrect: {
    backgroundColor: "#f0fdf4",
  },
  resultWrong: {
    backgroundColor: "#fef2f2",
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 4,
  },
  resultAnswer: {
    fontSize: 15,
    color: "#475569",
    marginBottom: 4,
  },
  resultStats: {
    fontSize: 13,
    color: "#94a3b8",
    marginTop: 4,
  },
  nextButton: {
    backgroundColor: "#2563eb",
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: "center",
    marginTop: 16,
  },
  nextButtonText: {
    color: "#fff",
    fontSize: 17,
    fontWeight: "700",
  },
});
