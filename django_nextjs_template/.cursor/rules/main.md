# Cursor Rules

## TypeScript/React Rules
```typescript
{
  "typescript": {
    "indent": 4,
    "maxLineLength": 140,
    "noDefaultExports": true,
    "componentNaming": "PascalCase",
    "importOrder": [
      "react",
      "next",
      "@mui",
      "@/components",
      "@/next_utils",
      "@/api",
      "relative"
    ]
  }
}
```

## File Organization
- Frontend code must be in `spa` directory
- Backend code must be in `backend` directory
- API types must be in `spa/api/apiTypes.ts`
- Utility functions must be in `spa/next_utils`
- Components must be in `spa/components`

## Component Rules
- Use Material UI components
- Use 4 spaces indentation
- No default exports for components
- Use TypeScript for all components
- Use React Hook Form for forms
- Use controlled components from `next_utils/fields`

## API Rules
- Use `useApi` from `apiClient.ts` for client components
- Use methods from `apiServer.ts` for server components
- Define API types in `apiTypes.ts`
- Use proper error handling

## Styling Rules
- Use Material UI's styling system
- Use the theme provider
- Follow the project's color scheme
- Use responsive design patterns

## Form Rules
- Use React Hook Form
- Use Generic Modal Form when possible
- Use controlled fields from `next_utils/fields`
- Implement proper validation

## Localization Rules
- Use react-intl for all text
- Update localization files for new strings
- Support all defined locales

## Performance Rules
- Implement proper memoization
- Avoid unnecessary rerenders
- Use proper loading states
- Optimize bundle size