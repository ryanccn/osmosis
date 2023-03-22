export interface RawStableDiffusionMetadata {
  model?: "stable diffusion";
  model_weights: string | null;
  model_hash?: string | null;
  app_id?: string | null;
  app_version?: string | null;
  image: {
    prompt: string;
    steps: number;
    cfg_scale: number;
    threshold?: number;
    perlin?: number;
    height: number;
    width: number;
    seed: number;
    seamless?: boolean;
    hires_fix?: boolean;
    type: string;
    postprocessing?: (
      | { type: "esrgan"; scale: number; strength: number }
      | { type: "gfpgan"; strength: number }
    )[];
    sampler: string;
    variations: unknown;
  };
}
