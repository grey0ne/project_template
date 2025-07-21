import createMiddleware from 'next-intl/middleware';
import { routing } from '@/next_utils/i18n/routing';
 
export default createMiddleware(routing);
 
export const config = {
    // Match only internationalized pathnames
    matcher: [
      '/((?!api|_next|.*\\..*).*)',
    ]
};