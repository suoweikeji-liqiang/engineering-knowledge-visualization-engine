import type {CharacterMotionProfile, CharacterPerformanceState, TopologyComposition} from '@repo/schemas';

export type TextFit = {
  fontSize: number;
  lineHeight: number;
  estimatedLines: number;
  fits: boolean;
};

export type TextFitOptions = {
  maxFontSize: number;
  minFontSize?: number;
  maxLines?: number;
  lineHeightRatio?: number;
  horizontalSafety?: number;
};

export const CARD_SYSTEM_V2 = {
  id: 'card-system-v2',
  indexTreatment: 'detached-badge',
  indexGap: 18,
  contentAlignment: 'intrinsic-centered',
  surfaceHierarchy: 'neutral-surface-with-semantic-rail',
  evidenceRelationship: 'source-connector-callout',
  minimumHorizontalPadding: 28,
} as const;

export const SCENE_GRAMMAR_V2 = {
  id: 'scene-grammar-v2',
  topologyCompositions: ['orbit', 'branch', 'quadrants', 'constellation', 'dashboard', 'hero-map'],
  minimumDistinctTopologyCompositions: 5,
  maximumSingleCompositionShare: 0.34,
  unknownCompositionPolicy: 'fail-review',
} as const;

export type {TopologyComposition};

export const XIAOLAN_PERFORMANCE_V1 = {
  id: 'xiaolan-performance-v1',
  states: ['investigate', 'recover', 'synthesize'],
  requiredFields: ['state', 'emotion', 'gesture', 'motionProfile', 'focusTarget'],
  motionProfiles: ['scan-and-mark', 'error-to-success', 'assemble-and-present'],
} as const;

export const XIAOLAN_PERFORMANCE_V2 = {
  ...XIAOLAN_PERFORMANCE_V1,
  id: 'xiaolan-performance-v2',
  minimumBeatsPerShot: 3,
  beatFields: ['id', 'cueIndex', 'pose', 'gaze', 'gesture', 'expression', 'asset', 'transition'],
  transitions: ['cut-in', 'match-cut', 'reaction-pop'],
  presentation: 'semantic-reaction-insert',
} as const;

export const XIAOLAN_STAGE_V3 = {
  id: 'xiaolan-stage-v3',
  presentation: 'transparent-anchored-actor',
  requiredFields: ['asset', 'intrinsicSize', 'pose', 'gaze', 'gesture', 'interactionAnchor', 'targetAnchor', 'interactionSfx', 'targetId', 'side', 'cueIndex', 'entrance', 'layer'],
  supportedVisualKinds: ['topology', 'code', 'bars', 'curve'],
  poses: ['pointing', 'thinking', 'presenting'],
  entrances: ['slide', 'rise', 'pop'],
  targetBinding: 'semantic-id',
  sourceBinding: 'normalized-gesture-anchor',
  targetPlacement: 'nearest-edge',
  connectorTiming: 'actor-first-then-tether',
  alphaRequired: true,
  minimumDistinctVisualKinds: 3,
} as const;

export type XiaolanPerformanceState = CharacterPerformanceState;
export type XiaolanMotionProfile = CharacterMotionProfile;

export function detachedBadgeX(cardWidth: number, badgeWidth: number): number {
  return -cardWidth / 2 - CARD_SYSTEM_V2.indexGap - badgeWidth / 2;
}

export function textUnits(text: string): number {
  return [...text].reduce((total, character) => {
    if (/\s/u.test(character)) return total + 0.34;
    if (/[\u3400-\u9fff]/u.test(character)) return total + 1;
    if (/[A-Z0-9]/u.test(character)) return total + 0.68;
    if (/[a-z]/u.test(character)) return total + 0.56;
    return total + 0.48;
  }, 0);
}

export function fitText(text: string, width: number, height: number, options: TextFitOptions): TextFit {
  const minFontSize = options.minFontSize ?? 14;
  const maxLines = options.maxLines ?? 2;
  const lineHeightRatio = options.lineHeightRatio ?? 1.24;
  const horizontalSafety = options.horizontalSafety ?? 0.88;
  const units = Math.max(1, textUnits(text));
  for (let fontSize = options.maxFontSize; fontSize >= minFontSize; fontSize -= 0.5) {
    const capacityPerLine = width * horizontalSafety / fontSize;
    const estimatedLines = Math.max(1, Math.ceil(units / capacityPerLine));
    const lineHeight = fontSize * lineHeightRatio;
    if (estimatedLines <= maxLines && estimatedLines * lineHeight <= height) {
      return {fontSize, lineHeight, estimatedLines, fits: true};
    }
  }
  const lineHeight = minFontSize * lineHeightRatio;
  return {
    fontSize: minFontSize,
    lineHeight,
    estimatedLines: Math.max(1, Math.ceil(units / (width * horizontalSafety / minFontSize))),
    fits: false,
  };
}

export function containSize(sourceWidth: number, sourceHeight: number, maxWidth: number, maxHeight: number) {
  if (sourceWidth <= 0 || sourceHeight <= 0 || maxWidth <= 0 || maxHeight <= 0) {
    throw new Error('containSize expects positive dimensions');
  }
  const scale = Math.min(maxWidth / sourceWidth, maxHeight / sourceHeight);
  return {width: sourceWidth * scale, height: sourceHeight * scale};
}

export const CHARACTER_SOURCE_SIZE = {width: 1672, height: 941} as const;
export const CHARACTER_VIEWPORT = {width: 824, height: 520} as const;
export const CHARACTER_CONTAINED_SIZE = containSize(
  CHARACTER_SOURCE_SIZE.width,
  CHARACTER_SOURCE_SIZE.height,
  CHARACTER_VIEWPORT.width,
  CHARACTER_VIEWPORT.height,
);

export const PERFORMANCE_POSE_SOURCE_SIZE = {width: 1376, height: 768} as const;
export const PERFORMANCE_POSE_VIEWPORT = {width: 268, height: 150} as const;
export const PERFORMANCE_POSE_CONTAINED_SIZE = containSize(
  PERFORMANCE_POSE_SOURCE_SIZE.width,
  PERFORMANCE_POSE_SOURCE_SIZE.height,
  PERFORMANCE_POSE_VIEWPORT.width,
  PERFORMANCE_POSE_VIEWPORT.height,
);
