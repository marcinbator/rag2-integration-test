export class AuthEndpointsServiceMock {
  verifyJWTToken(): {
    subscribe: (arg0: {
      next: (isValid: boolean) => void;
      error: () => void;
    }) => void;
  } {
    return {
      subscribe: ({ next, error }) => {
        next(true);
      },
    };
  }
}
