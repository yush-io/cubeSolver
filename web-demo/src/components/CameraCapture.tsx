import { Camera, RefreshCcw, ScanLine, Send, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { CSSProperties } from "react";

const FACE_PROMPTS = [
  { label: "White center", color: "#f4f1e8" },
  { label: "Red center", color: "#d9292f" },
  { label: "Green center", color: "#27a36a" },
  { label: "Yellow center", color: "#ffd21f" },
  { label: "Orange center", color: "#f47b20" },
  { label: "Blue center", color: "#2368c4" },
];

type CameraCaptureProps = {
  onSubmit: (photos: Blob[]) => void;
  onUseSample: () => void;
  isSolving: boolean;
};

export function CameraCapture({ onSubmit, onUseSample, isSolving }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [photos, setPhotos] = useState<Blob[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);
  const [cameraError, setCameraError] = useState("");

  useEffect(() => {
    let isMounted = true;

    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "environment" }, audio: false })
      .then((stream) => {
        if (!isMounted) return;
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch(() => {
        if (isMounted) setCameraError("Camera permission is needed to capture cube faces.");
      });

    return () => {
      isMounted = false;
      streamRef.current?.getTracks().forEach((track) => track.stop());
      previews.forEach(URL.revokeObjectURL);
    };
  }, []);

  function capturePhoto() {
    const video = videoRef.current;
    if (!video || photos.length >= 6) return;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth || 960;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) return;
      setPhotos((current) => [...current, blob]);
      setPreviews((current) => [...current, URL.createObjectURL(blob)]);
    }, "image/png");
  }

  function removePhoto(index: number) {
    URL.revokeObjectURL(previews[index]);
    setPhotos((current) => current.filter((_, photoIndex) => photoIndex !== index));
    setPreviews((current) => current.filter((_, photoIndex) => photoIndex !== index));
  }

  function resetPhotos() {
    previews.forEach(URL.revokeObjectURL);
    setPhotos([]);
    setPreviews([]);
  }

  const currentFace = FACE_PROMPTS[Math.min(photos.length, FACE_PROMPTS.length - 1)];
  const canSubmit = photos.length === 6 && !isSolving;
  const progress = Math.round((photos.length / FACE_PROMPTS.length) * 100);
  const intelligenceStatus = isSolving
    ? "Calibrating colors"
    : photos.length === 6
      ? "Ready to solve"
      : photos.length > 0
        ? "Detecting face alignment"
        : "Camera model waiting";

  return (
    <section className="capture-panel" aria-label="Camera capture">
      <div className="capture-status">
        <div className="progress-ring" style={{ "--progress": `${progress}%` } as CSSProperties}>
          <span>{photos.length}</span>
        </div>
        <div>
          <strong>{photos.length === 6 ? "Ready to solve" : currentFace.label}</strong>
          <p className="intelligence-line">
            <ScanLine size={14} />
            {intelligenceStatus}
          </p>
        </div>
      </div>

      <div className="camera-frame">
        <video ref={videoRef} autoPlay muted playsInline />
        <div className="scan-reticle" />
        <div className="corner-guide corner-guide-a" />
        <div className="corner-guide corner-guide-b" />
        <div className="corner-guide corner-guide-c" />
        <div className="corner-guide corner-guide-d" />
        {cameraError && <p className="camera-error">{cameraError}</p>}
      </div>

      <div className="capture-actions">
        <button type="button" className="icon-button primary" onClick={capturePhoto} disabled={photos.length >= 6}>
          <Camera size={18} />
          <span>Capture</span>
        </button>
        <button type="button" className="icon-button" onClick={resetPhotos} disabled={!photos.length || isSolving}>
          <RefreshCcw size={18} />
          <span>Reset</span>
        </button>
        <button type="button" className="icon-button" onClick={onUseSample} disabled={isSolving}>
          <ScanLine size={18} />
          <span>Sample</span>
        </button>
        <button type="button" className="icon-button solve" onClick={() => onSubmit(photos)} disabled={!canSubmit}>
          <Send size={18} />
          <span>{isSolving ? "Solving" : "Solve"}</span>
        </button>
      </div>

      <div className="photo-strip" aria-label="Captured photos">
        {FACE_PROMPTS.map((face, index) => (
          <button
            type="button"
            className="photo-slot"
            key={face.label}
            style={{ "--face-color": face.color } as CSSProperties}
            onClick={() => previews[index] && removePhoto(index)}
            aria-label={previews[index] ? `Remove ${face.label}` : face.label}
          >
            {previews[index] ? (
              <>
                <img src={previews[index]} alt="" />
                <X size={14} />
              </>
            ) : (
              <span>{index + 1}</span>
            )}
          </button>
        ))}
      </div>
    </section>
  );
}
