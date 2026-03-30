import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { useApi } from "@/lib/ApiContext";

export default function SettingsScreen() {
  const { apiUrl, setApiUrl } = useApi();
  const [url, setUrl] = useState(apiUrl ?? "");
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  const handleSave = async () => {
    const trimmed = url.trim();
    if (!trimmed) {
      Alert.alert("Error", "Please enter a valid API URL.");
      return;
    }

    setSaving(true);
    try {
      const testUrl = trimmed.endsWith("/") ? trimmed.slice(0, -1) : trimmed;
      const res = await fetch(`${testUrl}/topics`, { method: "GET" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      await setApiUrl(trimmed);
      if (router.canGoBack()) {
        router.back();
      }
    } catch {
      Alert.alert(
        "Connection Failed",
        "Could not connect to the API. Please check the URL and try again."
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <View style={styles.content}>
        <Text style={styles.title}>API Configuration</Text>
        <Text style={styles.subtitle}>
          Enter the URL of your Swedish quiz server
        </Text>

        <Text style={styles.label}>API URL</Text>
        <TextInput
          style={styles.input}
          value={url}
          onChangeText={setUrl}
          placeholder="http://192.168.1.5:8000"
          placeholderTextColor="#94a3b8"
          autoCapitalize="none"
          autoCorrect={false}
          keyboardType="url"
        />

        <TouchableOpacity
          style={[styles.button, saving && styles.buttonDisabled]}
          onPress={handleSave}
          disabled={saving}
        >
          <Text style={styles.buttonText}>
            {saving ? "Connecting…" : "Save & Connect"}
          </Text>
        </TouchableOpacity>

        {apiUrl && (
          <Text style={styles.currentUrl}>Current: {apiUrl}</Text>
        )}
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: "center",
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#1e293b",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 15,
    color: "#64748b",
    marginBottom: 32,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: "#475569",
    marginBottom: 8,
  },
  input: {
    backgroundColor: "#fff",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    borderWidth: 1,
    borderColor: "#e2e8f0",
    marginBottom: 20,
    color: "#1e293b",
  },
  button: {
    backgroundColor: "#2563eb",
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  currentUrl: {
    marginTop: 24,
    textAlign: "center",
    fontSize: 13,
    color: "#94a3b8",
  },
});
