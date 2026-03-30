import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { LearnResponse, NounWord, VerbWord, MiscWord } from "@/lib/types";

function CefrBadge({ level }: { level: number }) {
  const labels = ["", "A1", "A2", "B1", "B2", "C1", "C2"];
  const label = labels[level] || `C${level}`;
  return (
    <View style={styles.badge}>
      <Text style={styles.badgeText}>{label}</Text>
    </View>
  );
}

function FormRow({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.formRow}>
      <Text style={styles.formLabel}>{label}</Text>
      <Text style={styles.formValue}>{value}</Text>
    </View>
  );
}

function NounCard({ word }: { word: NounWord }) {
  return (
    <View style={styles.formsGrid}>
      <FormRow label="Indefinite" value={word.indefinite} />
      <FormRow label="Definite" value={word.definite} />
      <FormRow label="Plural" value={word.plural} />
      <FormRow label="Pl. definite" value={word.plural_definite} />
    </View>
  );
}

function VerbCard({ word }: { word: VerbWord }) {
  return (
    <View style={styles.formsGrid}>
      <FormRow label="Infinitive" value={word.infinitive} />
      <FormRow label="Present" value={word.present} />
      <FormRow label="Past" value={word.past} />
      <FormRow label="Supine" value={word.supine} />
      {word.imperative && <FormRow label="Imperative" value={word.imperative} />}
    </View>
  );
}

function MiscCard({ word }: { word: MiscWord }) {
  return (
    <View style={styles.formsGrid}>
      <FormRow label="Swedish" value={word.swedish} />
    </View>
  );
}

export default function WordCard({ data }: { data: LearnResponse }) {
  const { type, word } = data;

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <View style={styles.typeBadge}>
          <Text style={styles.typeText}>{type}</Text>
        </View>
        <CefrBadge level={word.cefr} />
      </View>

      {type === "noun" && <NounCard word={word as NounWord} />}
      {type === "verb" && <VerbCard word={word as VerbWord} />}
      {type === "misc" && <MiscCard word={word as MiscWord} />}

      <View style={styles.englishRow}>
        <Text style={styles.englishLabel}>English</Text>
        <Text style={styles.englishValue}>{word.english}</Text>
      </View>

      <View style={styles.metaRow}>
        <Text style={styles.metaText}>
          Frequency: {word.frequency.toFixed(1)}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 3,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  typeBadge: {
    backgroundColor: "#eff6ff",
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 8,
  },
  typeText: {
    fontSize: 13,
    fontWeight: "600",
    color: "#2563eb",
    textTransform: "capitalize",
  },
  badge: {
    backgroundColor: "#f0fdf4",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  badgeText: {
    fontSize: 13,
    fontWeight: "600",
    color: "#16a34a",
  },
  formsGrid: {
    borderTopWidth: 1,
    borderTopColor: "#f1f5f9",
    paddingTop: 12,
  },
  formRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#f8fafc",
  },
  formLabel: {
    fontSize: 14,
    color: "#64748b",
  },
  formValue: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1e293b",
  },
  englishRow: {
    marginTop: 16,
    backgroundColor: "#f8fafc",
    borderRadius: 10,
    padding: 14,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  englishLabel: {
    fontSize: 14,
    color: "#64748b",
  },
  englishValue: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1e293b",
  },
  metaRow: {
    marginTop: 12,
    alignItems: "center",
  },
  metaText: {
    fontSize: 12,
    color: "#94a3b8",
  },
});
