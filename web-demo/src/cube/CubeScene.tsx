import { Environment, OrbitControls, RoundedBox } from "@react-three/drei";
import { Canvas, useFrame } from "@react-three/fiber";
import { Bloom, EffectComposer } from "@react-three/postprocessing";
import { useEffect, useMemo, useRef, useState } from "react";
import { MathUtils, Quaternion, Vector3 } from "three";
import type { Group, Object3D } from "three";
import type { CubeMove } from "./moves";

type CubeSceneProps = {
  stage: "intro" | "capture" | "scramble" | "solve" | "done";
  activeMove?: CubeMove;
  moveToken: number;
  resetToken: number;
  playbackIndex: number;
};

const FACE_COLORS = {
  right: "#d9292f",
  left: "#f47b20",
  up: "#f4f1e8",
  down: "#ffd21f",
  front: "#27a36a",
  back: "#2368c4",
  core: "#121418",
};

type Coord = {
  x: number;
  y: number;
  z: number;
};

type CubeletState = Coord & {
  id: string;
  origin: Coord;
  quaternion: [number, number, number, number];
};

type MoveAnimation = {
  move: CubeMove;
  elapsed: number;
  duration: number;
  axis: Vector3;
  angle: number;
  layer: (cubelet: CubeletState) => boolean;
};

const SPACING = 0.58;
const IDENTITY_QUATERNION: [number, number, number, number] = [0, 0, 0, 1];

function Sticker({ position, rotation, color }: { position: [number, number, number]; rotation: [number, number, number]; color: string }) {
  return (
    <mesh position={position} rotation={rotation}>
      <planeGeometry args={[0.48, 0.48]} />
      <meshStandardMaterial color={color} roughness={0.42} metalness={0.08} />
    </mesh>
  );
}

function Cubelet({ cubelet, registerRef }: { cubelet: CubeletState; registerRef: (id: string, object: Object3D | null) => void }) {
  const { origin } = cubelet;
  return (
    <group ref={(object) => registerRef(cubelet.id, object)}>
      <RoundedBox args={[0.54, 0.54, 0.54]} radius={0.045} smoothness={3}>
        <meshStandardMaterial color={FACE_COLORS.core} roughness={0.58} metalness={0.18} />
      </RoundedBox>
      {origin.x === 1 && <Sticker position={[0.276, 0, 0]} rotation={[0, Math.PI / 2, 0]} color={FACE_COLORS.right} />}
      {origin.x === -1 && <Sticker position={[-0.276, 0, 0]} rotation={[0, -Math.PI / 2, 0]} color={FACE_COLORS.left} />}
      {origin.y === 1 && <Sticker position={[0, 0.276, 0]} rotation={[-Math.PI / 2, 0, 0]} color={FACE_COLORS.up} />}
      {origin.y === -1 && <Sticker position={[0, -0.276, 0]} rotation={[Math.PI / 2, 0, 0]} color={FACE_COLORS.down} />}
      {origin.z === 1 && <Sticker position={[0, 0, 0.276]} rotation={[0, 0, 0]} color={FACE_COLORS.front} />}
      {origin.z === -1 && <Sticker position={[0, 0, -0.276]} rotation={[0, Math.PI, 0]} color={FACE_COLORS.back} />}
    </group>
  );
}

function createCubelets(): CubeletState[] {
  const cubelets: CubeletState[] = [];
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        cubelets.push({
          id: `${x}-${y}-${z}`,
          x,
          y,
          z,
          origin: { x, y, z },
          quaternion: IDENTITY_QUATERNION,
        });
      }
    }
  }
  return cubelets;
}

function moveToAnimation(move: CubeMove): MoveAnimation {
  const face = move[0];
  const turnAmount = move.includes("2") ? Math.PI : Math.PI / 2;
  const direction = move.includes("'") ? 1 : -1;
  const angle = turnAmount * direction;

  if (face === "U") return { move, elapsed: 0, duration: 0.32, axis: new Vector3(0, 1, 0), angle, layer: (c) => c.y === 1 };
  if (face === "D") return { move, elapsed: 0, duration: 0.32, axis: new Vector3(0, -1, 0), angle, layer: (c) => c.y === -1 };
  if (face === "L") return { move, elapsed: 0, duration: 0.32, axis: new Vector3(-1, 0, 0), angle, layer: (c) => c.x === -1 };
  if (face === "R") return { move, elapsed: 0, duration: 0.32, axis: new Vector3(1, 0, 0), angle, layer: (c) => c.x === 1 };
  if (face === "F") return { move, elapsed: 0, duration: 0.32, axis: new Vector3(0, 0, 1), angle, layer: (c) => c.z === 1 };
  return { move, elapsed: 0, duration: 0.32, axis: new Vector3(0, 0, -1), angle, layer: (c) => c.z === -1 };
}

function roundCoord(value: number) {
  return MathUtils.clamp(Math.round(value), -1, 1);
}

function commitMove(cubelets: CubeletState[], animation: MoveAnimation): CubeletState[] {
  const turnQuaternion = new Quaternion().setFromAxisAngle(animation.axis, animation.angle);
  return cubelets.map((cubelet) => {
    if (!animation.layer(cubelet)) return cubelet;

    const coord = new Vector3(cubelet.x, cubelet.y, cubelet.z).applyAxisAngle(animation.axis, animation.angle);
    const baseQuaternion = new Quaternion(...cubelet.quaternion);
    const nextQuaternion = turnQuaternion.clone().multiply(baseQuaternion);

    return {
      ...cubelet,
      x: roundCoord(coord.x),
      y: roundCoord(coord.y),
      z: roundCoord(coord.z),
      quaternion: nextQuaternion.toArray() as [number, number, number, number],
    };
  });
}

function RubiksCube({ stage, activeMove, moveToken, resetToken, playbackIndex }: CubeSceneProps) {
  const groupRef = useRef<Group>(null);
  const cubeletRefs = useRef(new Map<string, Object3D>());
  const moveQueueRef = useRef<CubeMove[]>([]);
  const animationRef = useRef<MoveAnimation | null>(null);
  const latestCubeletsRef = useRef<CubeletState[]>([]);
  const [cubelets, setCubelets] = useState(createCubelets);

  latestCubeletsRef.current = cubelets;

  useEffect(() => {
    if (!activeMove) return;
    moveQueueRef.current.push(activeMove);
  }, [activeMove, moveToken]);

  useEffect(() => {
    if (stage !== "intro") return;
    setCubelets(createCubelets());
    moveQueueRef.current = [];
    animationRef.current = null;
  }, [stage]);

  useEffect(() => {
    setCubelets(createCubelets());
    moveQueueRef.current = [];
    animationRef.current = null;
  }, [resetToken]);

  function registerRef(id: string, object: Object3D | null) {
    if (object) {
      cubeletRefs.current.set(id, object);
    } else {
      cubeletRefs.current.delete(id);
    }
  }

  useFrame(({ clock }, delta) => {
    if (!groupRef.current) return;
    const elapsed = clock.getElapsedTime();
    const spinSpeed = stage === "intro" ? 1.8 : stage === "scramble" ? 1.15 : 0.14;
    groupRef.current.rotation.y += delta * spinSpeed;
    groupRef.current.rotation.z = stage === "intro" ? Math.sin(elapsed * 2.4) * 0.16 : 0.08;
    groupRef.current.rotation.x = Math.sin(elapsed * 0.55) * 0.13 + 0.42 + playbackIndex * 0.01;
    const targetScale = stage === "intro" ? 1.28 : stage === "capture" ? 0.72 : stage === "scramble" ? 1.08 : 1;
    groupRef.current.scale.lerp({ x: targetScale, y: targetScale, z: targetScale }, 0.06);

    if (!animationRef.current && moveQueueRef.current.length > 0) {
      const nextMove = moveQueueRef.current.shift();
      if (nextMove) animationRef.current = moveToAnimation(nextMove);
    }

    const animation = animationRef.current;
    const easedProgress = animation
      ? 1 - Math.pow(1 - Math.min(animation.elapsed / animation.duration, 1), 3)
      : 0;
    const animatedAngle = animation ? animation.angle * easedProgress : 0;
    const activeQuaternion = animation ? new Quaternion().setFromAxisAngle(animation.axis, animatedAngle) : null;

    latestCubeletsRef.current.forEach((cubelet) => {
      const object = cubeletRefs.current.get(cubelet.id);
      if (!object) return;

      const assemble = stage === "intro" ? Math.min(elapsed / 1.25, 1) : 1;
      const burst = stage === "intro" ? (1 - assemble) * 1.55 : 0;
      const basePosition = new Vector3(
        cubelet.x * SPACING + cubelet.origin.x * burst,
        cubelet.y * SPACING + cubelet.origin.y * burst,
        cubelet.z * SPACING + cubelet.origin.z * burst,
      );
      const baseQuaternion = new Quaternion(...cubelet.quaternion);

      if (animation?.layer(cubelet) && activeQuaternion) {
        object.position.copy(basePosition.applyAxisAngle(animation.axis, animatedAngle));
        object.quaternion.copy(activeQuaternion.clone().multiply(baseQuaternion));
      } else {
        object.position.copy(basePosition);
        object.quaternion.copy(baseQuaternion);
      }
    });

    if (animation) {
      animation.elapsed += delta;
      if (animation.elapsed >= animation.duration) {
        setCubelets((current) => commitMove(current, animation));
        animationRef.current = null;
      }
    }
  });

  return (
    <group ref={groupRef} rotation={[0.42, -0.72, 0.08]}>
      {cubelets.map((cubelet) => (
        <Cubelet key={cubelet.id} cubelet={cubelet} registerRef={registerRef} />
      ))}
    </group>
  );
}

export function CubeScene(props: CubeSceneProps) {
  return (
    <div className="cube-scene">
      <Canvas camera={{ position: [3.2, 2.2, 4.2], fov: 38 }}>
        <color attach="background" args={["#090b0f"]} />
        <ambientLight intensity={props.stage === "intro" ? 0.22 : 0.45} />
        <directionalLight position={[4, 5, 6]} intensity={props.stage === "intro" ? 4.5 : 3.2} />
        <directionalLight position={[-3, -2, -4]} intensity={0.85} color="#43c6ac" />
        <RubiksCube {...props} />
        <Environment preset="city" />
        <EffectComposer>
          <Bloom intensity={props.stage === "intro" || props.stage === "scramble" ? 0.5 : 0.28} luminanceThreshold={0.36} luminanceSmoothing={0.55} />
        </EffectComposer>
        <OrbitControls enableZoom={false} enablePan={false} autoRotate={false} />
      </Canvas>
    </div>
  );
}
