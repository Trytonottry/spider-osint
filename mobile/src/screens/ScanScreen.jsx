import React, { useState } from 'react';
import { View, TextInput, Button, Text, Alert } from 'react-native';
import Voice from 'react-native-voice';
import axios from 'axios';
import VoiceAssistant from './VoiceAssistant';

const askAssistant = async () => {
  try {
    const res = await axios.post('http://your-server:8000/ask', {
      query: "Где может жить этот человек?",
      context: JSON.stringify(results)
    });
    Alert.alert("Аналитика", res.data.answer);
  } catch (e) {
    Alert.alert("Ошибка", "Не удалось связаться с ИИ");
  }
};

const ScanScreen = () => {
  const [target, setTarget] = useState('');
  const [isListening, setIsListening] = useState(false);

  const startScan = async () => {
    try {
      const res = await axios.post('http://your-server:8000/scan', { target });
      Alert.alert('Готово', 'Сканирование запущено');
    } catch (err) {
      Alert.alert('Ошибка', err.message);
    }
  };

  // Голосовой ввод
  Voice.onSpeechResults = (e) => {
    if (e.value && e.value.length > 0) {
      setTarget(e.value[0]);
      setIsListening(false);
    }
  };

  const startVoice = async () => {
    setIsListening(true);
    await Voice.start('ru');
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Цель:</Text>
      <TextInput value={target} onChangeText={setTarget} placeholder="Email, имя..." />
      <Button title="Сканировать" onPress={startScan} />
      <Button title={isListening ? "Слушаю..." : "🎤 Голос"} onPress={startVoice} />
      <VoiceAssistant />
    </View>
  );
};

export default ScanScreen;