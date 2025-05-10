export class AuthEndpointsServiceMock {
  verifyJWTToken(): {
    subscribe: (arg0: {
      next: (isValid: boolean) => void;
      error: () => void;
    }) => void;
  } {
    return {
      subscribe: ({ next, error }) => {
        const isValid = localStorage.getItem("jwtToken") !== null;
        if (isValid) {
          next(true);
        } else {
          error();
        }
      },
    };
  }
}
