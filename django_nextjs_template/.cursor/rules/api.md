# API Rules

## Client-Side API Calls
```typescript
// Use useApi hook for data fetching
import { useApi } from '@/next_utils/apiClient'
const { data, error, isLoading } = useApi('/api/endpoint');

// Use proper error handling
if (error) {
    // Handle error
}

// Use proper loading states
if (isLoading) {
    return <LoadingComponent />;
}
```

## Server-Side API Calls
```typescript
// Use apiServer methods
import { apiRequest, apiGet } from '@/next_utils/apiServer'
const data = await apiGet('/api/endpoint');

```

## API Types
- API Types is defined in `apiTypes.ts`