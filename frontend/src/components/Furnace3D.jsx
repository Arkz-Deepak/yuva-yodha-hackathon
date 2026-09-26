import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function Furnace3D({ 
  temperature = 30, 
  targetTemp = 1520, 
  state = "IDLE", 
  lidIsClosed = true, 
  tiltAngle = 0,
  powerKw = 0,
  radiationLossKw = 0
}) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const furnaceGroupRef = useRef(null);
  const lidMeshRef = useRef(null);
  const moltenMeshRef = useRef(null);
  const meltLightRef = useRef(null);
  const heatParticlesRef = useRef(null);
  const pourStreamRef = useRef(null);
  const isDraggingRef = useRef(false);
  const prevMouseRef = useRef({ x: 0, y: 0 });
  const rotationRef = useRef({ x: 0.35, y: -0.6 });

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Scene & Camera
    const width = container.clientWidth;
    const height = container.clientHeight || 450;
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 3.2, 5.5);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x222a38, 1.8);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, 1.4);
    dirLight1.position.set(5, 8, 4);
    dirLight1.castShadow = true;
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x406080, 0.8);
    dirLight2.position.set(-5, 4, -4);
    scene.add(dirLight2);

    // Inner Molten Point Light (Dynamic Heat Glow)
    const meltLight = new THREE.PointLight(0xff4400, 1.0, 6);
    meltLight.position.set(0, 1.0, 0);
    scene.add(meltLight);
    meltLightRef.current = meltLight;

    // Shop Floor Grid / Base Pad
    const gridHelper = new THREE.GridHelper(10, 20, 0x1e293b, 0x0f172a);
    gridHelper.position.y = -1.2;
    scene.add(gridHelper);

    // Foundation Base Pedestal
    const baseGeo = new THREE.CylinderGeometry(1.6, 1.8, 0.4, 32);
    const baseMat = new THREE.MeshStandardMaterial({ color: 0x1e2634, roughness: 0.8 });
    const baseMesh = new THREE.Mesh(baseGeo, baseMat);
    baseMesh.position.y = -1.0;
    scene.add(baseMesh);

    // Tilting Furnace Assembly Group (Pivots at Trunnion axis)
    const furnaceGroup = new THREE.Group();
    furnaceGroup.position.set(0, 0.1, 0);
    scene.add(furnaceGroup);
    furnaceGroupRef.current = furnaceGroup;

    // 1. Outer Steel Shell
    const shellGeo = new THREE.CylinderGeometry(1.05, 1.0, 2.0, 32, 1, true);
    const shellMat = new THREE.MeshStandardMaterial({ 
      color: 0x2d3748, 
      metalness: 0.8, 
      roughness: 0.35, 
      side: THREE.DoubleSide 
    });
    const shell = new THREE.Mesh(shellGeo, shellMat);
    furnaceGroup.add(shell);

    // Bottom cap
    const bottomGeo = new THREE.CylinderGeometry(1.0, 1.0, 0.1, 32);
    const bottom = new THREE.Mesh(bottomGeo, shellMat);
    bottom.position.y = -1.0;
    furnaceGroup.add(bottom);

    // 2. Copper Induction Coils (6 helical rings)
    const copperMat = new THREE.MeshStandardMaterial({
      color: 0xb87333,
      metalness: 0.9,
      roughness: 0.2
    });
    for (let i = -0.7; i <= 0.7; i += 0.28) {
      const coilGeo = new THREE.TorusGeometry(1.15, 0.05, 16, 40);
      const coilMesh = new THREE.Mesh(coilGeo, copperMat);
      coilMesh.rotation.x = Math.PI / 2;
      coilMesh.position.y = i;
      furnaceGroup.add(coilMesh);
    }

    // 3. Refractory Ceramic Lining (Interior wall)
    const liningGeo = new THREE.CylinderGeometry(0.85, 0.8, 1.9, 32, 1, true);
    const liningMat = new THREE.MeshStandardMaterial({ 
      color: 0xd97706, 
      roughness: 0.9,
      side: THREE.BackSide 
    });
    const lining = new THREE.Mesh(liningGeo, liningMat);
    furnaceGroup.add(lining);

    // 4. Molten Metal Bath
    const moltenGeo = new THREE.CylinderGeometry(0.83, 0.78, 1.4, 32);
    const moltenMat = new THREE.MeshStandardMaterial({
      color: 0x4a5568,
      emissive: 0x000000,
      emissiveIntensity: 0.0,
      roughness: 0.4
    });
    const molten = new THREE.Mesh(moltenGeo, moltenMat);
    molten.position.y = -0.2;
    furnaceGroup.add(molten);
    moltenMeshRef.current = molten;

    // 5. Tapping Spout / Lip
    const spoutGeo = new THREE.ConeGeometry(0.3, 0.5, 4);
    spoutGeo.rotateZ(-Math.PI / 2);
    const spout = new THREE.Mesh(spoutGeo, shellMat);
    spout.position.set(0.95, 0.95, 0);
    furnaceGroup.add(spout);

    // 6. Insulated Furnace Lid (Pivots at rear hinge)
    const lidGroup = new THREE.Group();
    lidGroup.position.set(-0.85, 1.05, 0); // Hinge position
    furnaceGroup.add(lidGroup);

    const lidDiscGeo = new THREE.CylinderGeometry(1.08, 1.08, 0.12, 32);
    const lidMat = new THREE.MeshStandardMaterial({ 
      color: 0x334155, 
      metalness: 0.7, 
      roughness: 0.4 
    });
    const lidDisc = new THREE.Mesh(lidDiscGeo, lidMat);
    lidDisc.position.set(0.85, 0.06, 0); // Offset from hinge
    lidGroup.add(lidDisc);
    lidMeshRef.current = lidGroup;

    // 7. Heat Radiation Particles / Waves (Active when lid is open & hot)
    const particleCount = 40;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 1.2;
      particlePositions[i * 3 + 1] = 1.1 + Math.random() * 1.5;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 1.2;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0xff3b00,
      size: 0.08,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    });
    const heatParticles = new THREE.Points(particleGeo, particleMat);
    furnaceGroup.add(heatParticles);
    heatParticlesRef.current = heatParticles;

    // 8. Tapping Pour Stream (Liquid metal stream falling into ladle)
    const pourGeo = new THREE.CylinderGeometry(0.04, 0.08, 2.0, 12);
    const pourMat = new THREE.MeshStandardMaterial({
      color: 0xffdd44,
      emissive: 0xff6600,
      emissiveIntensity: 2.0
    });
    const pourStream = new THREE.Mesh(pourGeo, pourMat);
    pourStream.position.set(1.4, -0.2, 0);
    pourStream.visible = false;
    scene.add(pourStream);
    pourStreamRef.current = pourStream;

    // Mouse Interaction for smooth 3D Orbiting
    const handleMouseDown = (e) => {
      isDraggingRef.current = true;
      prevMouseRef.current = { x: e.clientX, y: e.clientY };
    };

    const handleMouseMove = (e) => {
      if (!isDraggingRef.current) return;
      const dx = e.clientX - prevMouseRef.current.x;
      const dy = e.clientY - prevMouseRef.current.y;
      rotationRef.current.y += dx * 0.008;
      rotationRef.current.x = Math.max(-0.2, Math.min(1.0, rotationRef.current.x + dy * 0.008));
      prevMouseRef.current = { x: e.clientX, y: e.clientY };
    };

    const handleMouseUp = () => {
      isDraggingRef.current = false;
    };

    container.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    // Animation Loop
    let animationFrameId;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      // Camera positioning based on orbital rotation
      const r = 5.2;
      camera.position.x = r * Math.sin(rotationRef.current.y) * Math.cos(rotationRef.current.x);
      camera.position.z = r * Math.cos(rotationRef.current.y) * Math.cos(rotationRef.current.x);
      camera.position.y = r * Math.sin(rotationRef.current.x) + 0.6;
      camera.lookAt(0, 0.4, 0);

      // Animate heat particles floating upward
      if (heatParticlesRef.current && heatParticlesRef.current.visible) {
        const positions = heatParticlesRef.current.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
          positions[i * 3 + 1] += delta * 1.2;
          if (positions[i * 3 + 1] > 2.8) {
            positions[i * 3 + 1] = 1.1;
            positions[i * 3] = (Math.random() - 0.5) * 1.0;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 1.0;
          }
        }
        heatParticlesRef.current.geometry.attributes.position.needsUpdate = true;
      }

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight || 450;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      container.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('resize', handleResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Update dynamic properties on telemetry state change
  useEffect(() => {
    // 1. Temperature-based color interpolation
    // Ambient (<300°C) -> Dull red (600°C) -> Cherry (900°C) -> Bright Orange (1200°C) -> Incandescent Yellow-White (1520°C)
    const t = Math.max(30, Math.min(1600, temperature));
    let hexColor = 0x4a5568; // dark cold steel
    let emissiveColor = 0x000000;
    let emissiveIntensity = 0.0;
    let lightIntensity = 0.0;

    if (t > 400 && t <= 750) {
      hexColor = 0x8b1e0f; // dull dark red
      emissiveColor = 0x5a0d05;
      emissiveIntensity = 0.4;
      lightIntensity = 0.3;
    } else if (t > 750 && t <= 1100) {
      hexColor = 0xd9480f; // cherry orange
      emissiveColor = 0xcc3300;
      emissiveIntensity = 0.8;
      lightIntensity = 0.8;
    } else if (t > 1100 && t <= 1400) {
      hexColor = 0xf59f00; // fiery bright orange
      emissiveColor = 0xf57c00;
      emissiveIntensity = 1.4;
      lightIntensity = 1.6;
    } else if (t > 1400) {
      hexColor = 0xfff3bf; // incandescent molten steel
      emissiveColor = 0xffaa00;
      emissiveIntensity = 2.2;
      lightIntensity = 2.5;
    }

    if (moltenMeshRef.current) {
      moltenMeshRef.current.material.color.setHex(hexColor);
      moltenMeshRef.current.material.emissive.setHex(emissiveColor);
      moltenMeshRef.current.material.emissiveIntensity = emissiveIntensity;
    }

    if (meltLightRef.current) {
      meltLightRef.current.color.setHex(emissiveColor);
      meltLightRef.current.intensity = lightIntensity;
    }

    // 2. Lid position (Closed = 0 deg, Open = 80 deg rotation around hinge)
    if (lidMeshRef.current) {
      const targetLidAngle = lidIsClosed ? 0.0 : -1.4;
      lidMeshRef.current.rotation.z = targetLidAngle;
    }

    // 3. Heat radiation loss particles (Visible when lid is OPEN and bath is HOT)
    if (heatParticlesRef.current) {
      heatParticlesRef.current.visible = !lidIsClosed && temperature > 700;
    }

    // 4. Hydraulic Tilt for Tapping
    if (furnaceGroupRef.current) {
      const radTilt = (tiltAngle * Math.PI) / 180;
      furnaceGroupRef.current.rotation.z = radTilt;
    }

    // 5. Pour stream during tapping
    if (pourStreamRef.current) {
      pourStreamRef.current.visible = state === "TAPPING" && tiltAngle > 15;
    }

  }, [temperature, targetTemp, state, lidIsClosed, tiltAngle, powerKw]);

  return (
    <div className="relative w-full h-[460px] rounded-xl overflow-hidden bg-gradient-to-b from-[#0c121d] to-[#070a0f] border border-slate-800 shadow-2xl">
      {/* 3D Canvas Mount */}
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Floating 3D Twin HUD Overlays */}
      <div className="absolute top-3 left-4 pointer-events-none">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs uppercase tracking-wider font-semibold text-emerald-400">
            3D INDUCTION FURNACE TWIN (1.5 MT)
          </span>
        </div>
        <div className="mt-1 flex items-baseline gap-2">
          <span className="text-2xl font-bold font-mono text-white">{temperature.toFixed(0)}°C</span>
          <span className="text-xs text-slate-400">/ Target {targetTemp}°C</span>
        </div>
      </div>

      {/* Lid & Radiation Status Pill */}
      <div className="absolute top-3 right-4 pointer-events-none">
        <div className={`px-3 py-1 rounded-full text-xs font-semibold border flex items-center gap-1.5 ${
          lidIsClosed 
            ? 'bg-emerald-950/70 border-emerald-600/50 text-emerald-300' 
            : 'bg-rose-950/80 border-rose-600/60 text-rose-300 animate-pulse'
        }`}>
          <span>{lidIsClosed ? '🛡️ LID CLOSED' : '⚠️ LID OPEN'}</span>
          <span>•</span>
          <span>{lidIsClosed ? 'Radiation Minimized' : `Loss: +${radiationLossKw} kW`}</span>
        </div>
      </div>

      {/* Tilt Angle & Drag instructions */}
      <div className="absolute bottom-3 left-4 pointer-events-none text-[11px] text-slate-400 flex items-center gap-3">
        <span>🔄 Drag to rotate 3D view</span>
        {tiltAngle > 0 && (
          <span className="text-amber-400 font-mono font-medium">Hydraulic Tilt: {tiltAngle.toFixed(1)}°</span>
        )}
      </div>

      {/* Real-time State Badge */}
      <div className="absolute bottom-3 right-4 pointer-events-none">
        <span className={`px-3 py-1 rounded text-xs font-mono font-bold tracking-wider uppercase ${
          state === 'HOLDING' ? 'bg-rose-600 text-white animate-pulse' :
          state === 'MELTING' ? 'bg-amber-600 text-white' :
          state === 'TAPPING' ? 'bg-orange-600 text-white' :
          state === 'REFINING' ? 'bg-sky-600 text-white' : 'bg-slate-700 text-slate-200'
        }`}>
          {state}
        </span>
      </div>
    </div>
  );
}
