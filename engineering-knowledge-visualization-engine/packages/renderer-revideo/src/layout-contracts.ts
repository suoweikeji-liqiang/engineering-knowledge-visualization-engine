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
