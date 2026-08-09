import React, { useState, useEffect, useRef } from "react";
import {
  Home,
  User,
  Settings,
  Heart,
  Bell,
  Trash,
  Mail,
  Star,
  MapPin,
  Camera,
  Video,
  Music,
  Calendar,
  Compass,
  ShoppingCart,
  Search,
  Info,
  Sparkles,
  Download
} from "lucide-react";

export const PhoneCameraComponent = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [captured, setCaptured] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      setError("Kamera izni verilmedi veya desteklenmiyor.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const takePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.videoWidth || 640;
      canvas.height = videoRef.current.videoHeight || 480;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        setCaptured(canvas.toDataURL("image/png"));
        stopCamera();
      }
    }
  };

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  return (
    <div className="p-3 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-150 dark:border-zinc-800 rounded-2xl flex flex-col gap-2">
      <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-wide flex items-center gap-1">📸 Canlı Kamera Eklentisi</span>
      {captured ? (
        <div className="relative rounded-xl overflow-hidden shadow-inner aspect-video">
          <img src={captured} className="w-full h-full object-cover" alt="Captured" />
          <button 
            onClick={() => { setCaptured(null); startCamera(); }}
            className="absolute bottom-2 right-2 bg-indigo-600 text-white font-bold text-[9px] px-2.5 py-1 rounded-lg"
          >
            Yeniden Çek
          </button>
        </div>
      ) : stream ? (
        <div className="relative rounded-xl overflow-hidden shadow-inner aspect-video bg-black">
          <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover" />
          <button 
            onClick={takePhoto}
            className="absolute bottom-2 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full border-2 border-white bg-red-600 flex items-center justify-center shadow-lg active:scale-95 transition"
          />
        </div>
      ) : (
        <div className="aspect-video bg-zinc-200 dark:bg-zinc-800 rounded-xl flex flex-col items-center justify-center text-center gap-2 p-4">
          {error ? (
            <span className="text-[9px] text-red-500 font-medium">{error}</span>
          ) : (
            <>
              <span className="text-[9px] text-zinc-500">Kamera kapalı</span>
              <button 
                onClick={startCamera}
                className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-[9px] px-3 py-1.5 rounded-lg active:scale-95 transition"
              >
                Kamerayı Aç
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export const PhoneAudioPlayer = ({ url }: { url: string; key?: any }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <div className="p-3 bg-zinc-50 dark:bg-zinc-850/60 border border-zinc-150 dark:border-zinc-800 rounded-2xl flex items-center justify-between gap-3 shadow-sm text-left">
      <button 
        onClick={() => setIsPlaying(!isPlaying)}
        className="w-8 h-8 rounded-full bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white flex items-center justify-center shadow transition-all shrink-0"
      >
        {isPlaying ? <span className="text-[10px] font-bold">⏸</span> : <span className="text-[10px] font-bold pl-0.5">▶</span>}
      </button>
      <div className="flex-1 flex flex-col gap-1 min-w-0">
        <span className="text-[10px] font-bold text-zinc-700 dark:text-zinc-300 truncate">Ses Çalar: {url.split("/").pop()}</span>
        <div className="flex gap-0.5 items-end h-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18].map((i) => (
            <div 
              key={i} 
              className={`bg-indigo-500 rounded-full w-1 transition-all duration-300`} 
              style={{ 
                height: isPlaying ? `${Math.floor(Math.random() * 12) + 4}px` : "4px",
              }}
            />
          ))}
        </div>
      </div>
      <span className="text-[8px] text-zinc-400 self-end">00:15</span>
    </div>
  );
};

export const getIconComponent = (name: string) => {
  const iconName = name.toLowerCase().trim();
  switch (iconName) {
    case "ev":
    case "home":
      return <Home className="w-5 h-5" />;
    case "profil":
    case "kullanici":
    case "user":
      return <User className="w-5 h-5" />;
    case "ayarlar":
    case "settings":
      return <Settings className="w-5 h-5" />;
    case "kalp":
    case "heart":
      return <Heart className="w-5 h-5" />;
    case "bildirim":
    case "zil":
    case "bell":
      return <Bell className="w-5 h-5" />;
    case "cop":
    case "trash":
      return <Trash className="w-5 h-5" />;
    case "eposta":
    case "mail":
      return <Mail className="w-5 h-5" />;
    case "yildiz":
    case "star":
      return <Star className="w-5 h-5" />;
    case "harita":
    case "pin":
    case "map":
      return <MapPin className="w-5 h-5" />;
    case "kamera":
    case "camera":
      return <Camera className="w-5 h-5" />;
    case "video":
      return <Video className="w-5 h-5" />;
    case "ses":
    case "muzik":
    case "music":
      return <Music className="w-5 h-5" />;
    case "takvim":
    case "calendar":
      return <Calendar className="w-5 h-5" />;
    case "pusula":
    case "compass":
      return <Compass className="w-5 h-5" />;
    case "sepet":
    case "cart":
    case "shopping-cart":
      return <ShoppingCart className="w-5 h-5" />;
    case "arama":
    case "search":
      return <Search className="w-5 h-5" />;
    case "bilgi":
    case "info":
      return <Info className="w-5 h-5" />;
    default:
      return <Sparkles className="w-5 h-5" />;
  }
};
