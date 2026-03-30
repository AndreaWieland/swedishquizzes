import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  FlatList,
  StyleSheet,
} from "react-native";
import { Topic } from "@/lib/types";

interface Props {
  topics: Topic[];
  selected: string | null;
  onSelect: (name: string) => void;
}

export default function TopicPicker({ topics, selected, onSelect }: Props) {
  const [visible, setVisible] = useState(false);

  const selectedTopic = topics.find((t) => t.name === selected);

  return (
    <View>
      <TouchableOpacity style={styles.button} onPress={() => setVisible(true)}>
        <Text style={styles.buttonText}>
          {selectedTopic ? selectedTopic.display_name : "Select a topic…"}
        </Text>
        <Text style={styles.chevron}>▼</Text>
      </TouchableOpacity>

      <Modal visible={visible} transparent animationType="fade">
        <TouchableOpacity
          style={styles.overlay}
          activeOpacity={1}
          onPress={() => setVisible(false)}
        >
          <View style={styles.dropdown}>
            <Text style={styles.dropdownTitle}>Choose Topic</Text>
            <FlatList
              data={topics}
              keyExtractor={(item) => item.name}
              renderItem={({ item }) => (
                <TouchableOpacity
                  style={[
                    styles.option,
                    item.name === selected && styles.optionSelected,
                  ]}
                  onPress={() => {
                    onSelect(item.name);
                    setVisible(false);
                  }}
                >
                  <Text
                    style={[
                      styles.optionText,
                      item.name === selected && styles.optionTextSelected,
                    ]}
                  >
                    {item.display_name}
                  </Text>
                  <Text style={styles.optionCount}>
                    {item.counts.total} words
                  </Text>
                </TouchableOpacity>
              )}
            />
          </View>
        </TouchableOpacity>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: "#fff",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderWidth: 1,
    borderColor: "#e2e8f0",
  },
  buttonText: {
    fontSize: 16,
    color: "#1e293b",
  },
  chevron: {
    fontSize: 12,
    color: "#94a3b8",
  },
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    paddingHorizontal: 32,
  },
  dropdown: {
    backgroundColor: "#fff",
    borderRadius: 16,
    maxHeight: 400,
    paddingVertical: 8,
  },
  dropdownTitle: {
    fontSize: 17,
    fontWeight: "600",
    color: "#1e293b",
    textAlign: "center",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#f1f5f9",
  },
  option: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: "#f1f5f9",
  },
  optionSelected: {
    backgroundColor: "#eff6ff",
  },
  optionText: {
    fontSize: 16,
    color: "#1e293b",
  },
  optionTextSelected: {
    color: "#2563eb",
    fontWeight: "600",
  },
  optionCount: {
    fontSize: 13,
    color: "#94a3b8",
  },
});
