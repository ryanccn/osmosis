export const multiplesOf64 = [
  64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960,
  1024, 1088, 1152, 1216, 1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792,
  1856, 1920, 1984, 2048,
];

export const schedulers = {
  DDIM: "DDIM",
  DDPM: "DDPM",
  PNDM: "PNDM",
  LMSDiscrete: "LMS Discrete",
  EulerDiscrete: "Euler Discrete",
  EulerAncestralDiscrete: "Euler Ancestral Discrete",
  DPMSolverSinglestep: "DPM Solver Singlestep",
  DPMSolverMultistep: "DPM Solver Multistep",
  KDPM2Discrete: "DPM2 Discrete (Karras)",
  KDPM2AncestralDiscrete: "DPM2 Ancestral Discrete (Karras)",
  UniPCMultistep: "UniPC",
};
