import React, { useState } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import Voice from 'react-native-voice';
import axios from 'axios';

const VoiceAssistant = () => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');

  Voice.onSpeechResults = (e) => {
    if (e.value && e.value.length > 0) {
      const text = e.value[0];
      setTranscript(text);
      queryAssistant(text);
      setIsListening(false);
    }
  };

  const queryAssistant = async (question) => {
    try {
      const res = await axios.post('http://your-server:8000/ask', {
        query: question,
        context: JSON.stringify(global.spiderContext || {})
      });
      Alert.alert("SPIDER", res.data.answer);
    } catch (err) {
      Alert.alert("Ошибка", "Не удалось связаться с ИИ");
    }
  };

  const startListening = async () => {
    setIsListening(true);
    setTranscript('');
    try {
      await Voice.start('ru');
    } catch (e) {
      Alert.alert("Ошибка", e.message);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>🎙️ Спросите SPIDER:</Text>
      <Button
        title={isListening ? "Слушаю..." : "Говорить"}
        onPress={startListening}
        disabled={isListening}
      />
      {transcript ? <Text style={{ marginTop: 10 }}>{transcript}</Text> : null}
    </View>
  );
};

export default VoiceAssistant;