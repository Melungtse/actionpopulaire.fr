import { ReferralModal } from "./ReferralModal";

export default {
  component: ReferralModal,
  title: "Layout/PushModal/ReferralModal",
};

const Template = ReferralModal;

export const Default = Template.bind({});
Default.args = {
  referralURL: "#referral",
  shouldShow: true,
  onClose: () => {},
};
