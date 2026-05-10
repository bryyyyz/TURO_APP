<script setup>
import { computed, useAttrs } from 'vue';
import { ICON_PATHS } from './iconPaths';

defineOptions({ inheritAttrs: false });

const props = defineProps({
  /** Key in ICON_PATHS (camelCase) */
  name: { type: String, required: true },
  /** Pixel width & height */
  size: { type: [Number, String], default: 24 },
  /** Outline stroke width */
  strokeWidth: { type: [Number, String], default: 2 },
  /** Use solid fill (e.g. rating star) instead of outline */
  filled: { type: Boolean, default: false },
});

const attrs = useAttrs();

const elements = computed(() => ICON_PATHS[props.name] || []);

const svgClass = computed(() => {
  const cls = attrs.class;
  if (!cls) return 'turo-icon';
  return ['turo-icon', cls];
});

const numericSize = computed(() =>
  typeof props.size === 'string' ? parseFloat(props.size) || 24 : props.size
);
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    :width="numericSize"
    :height="numericSize"
    viewBox="0 0 24 24"
    :class="svgClass"
    :stroke="filled ? 'none' : 'currentColor'"
    :fill="filled ? 'currentColor' : 'none'"
    :stroke-width="filled ? 0 : strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    focusable="false"
    v-bind="Object.fromEntries(Object.entries(attrs).filter(([k]) => k !== 'class'))"
  >
    <template v-for="(el, i) in elements" :key="i">
      <path v-if="el.type === 'path'" :d="el.d" />
      <circle
        v-else-if="el.type === 'circle'"
        :cx="el.cx"
        :cy="el.cy"
        :r="el.r"
      />
      <rect
        v-else-if="el.type === 'rect'"
        :x="el.x"
        :y="el.y"
        :width="el.width"
        :height="el.height"
        :rx="el.rx"
        :ry="el.ry"
      />
      <line
        v-else-if="el.type === 'line'"
        :x1="el.x1"
        :y1="el.y1"
        :x2="el.x2"
        :y2="el.y2"
      />
      <polyline
        v-else-if="el.type === 'polyline'"
        :points="el.points"
      />
    </template>
  </svg>
</template>
