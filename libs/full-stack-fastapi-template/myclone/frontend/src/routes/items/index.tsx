import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";

import { readItemsV1ItemsGet } from "../../client/sdk.gen";

export const Route = createFileRoute("/items/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["todos"],
    queryFn: readItemsV1ItemsGet,
  });

  console.log("DEBUG", isPending, isError, data, error);

  if (isPending) {
    return <div>Pending</div>;
  }

  return (
    <div>
      <ul>
        {data.data.data.map((item) => (
          <li key={item.id}>
            {item.title}: {item.description}
          </li>
        ))}
      </ul>
    </div>
  );
}
