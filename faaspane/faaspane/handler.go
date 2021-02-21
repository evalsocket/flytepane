package function

import (
	"context"

	"github.com/lyft/flyteidl/clients/go/admin"
	"github.com/lyft/flyteidl/gen/pb-go/flyteidl/core"
)

// Handle a serverless request
func Handle(req []byte) string {
	ctx := context.Background()
	var input []byte
	query := r.URL.Query()
	adminClient, err := admin.InitializeAdminClientFromConfig(ctx)
	if err != nil {
		return err
	}

	executionList, err := cmdCtx.AdminClient().CreateExecution(ctx, &admin.ExecutionCreateRequest{
		Project: "flytesancks",
		Domain:  "development",
		Name:    "datapane.datapane.datapane_workflow",
		Spec: &admin.ExecutionSpec{
			Inputs: &core.LiteralMap{
				Literals: map[string]*core.Literal{
					"url": &core.Literal{
						Value: "https://covid.ourworldindata.org/data/owid-covid-data.csv",
					},
				},
			},
		},
	})
	if err != nil {
		return err
	}
}
